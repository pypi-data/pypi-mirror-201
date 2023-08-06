#include "rw.h"
#include <iostream>
#ifdef USE_MAGMA
#include "magma_v2.h"
#include "magmasparse.h"
#endif

typedef double element_type;

static size_t toLinear(Eigen::Vector2i dim, Eigen::Vector2i pos) {
    return dim(1) * pos(0) + pos(1);
}
#ifdef USE_MAGMA
#define CHECK_MAGMA_ERROR(val) { magma_int_t e = val; if(e > 0) throw RWException(magma_strerror(e)); }

static magma_d_matrix eigen_to_magma_sparse(Eigen::SparseMatrix<double, Eigen::ColMajor, magma_index_t>& mat, magma_queue_t queue) {
    magma_index_t* rows_ptr = mat.outerIndexPtr();
    magma_index_t* cols_ptr = mat.innerIndexPtr();
    double* data_ptr = mat.valuePtr();
    static_assert(sizeof(magma_index_t) == sizeof(*mat.outerIndexPtr()));

    magma_d_matrix mat_m;
    CHECK_MAGMA_ERROR(magma_dcsrset(mat.rows(), mat.cols(), rows_ptr, cols_ptr, data_ptr, &mat_m, queue));
    return mat_m;
}
#endif

std::pair<Image<uint32_t, 1>,std::vector<Image<float, 1>>> run_rw(const Image<float, 1> weights_horizontal, const Image<float, 1> weights_vertical, const Image<uint32_t, 1>& labels, size_t num_classes) {
    int rows = labels.rows();
    int cols = labels.cols();
    assert(weights_horizontal.rows() == rows);
    assert(weights_horizontal.cols() == cols-1);
    assert(weights_vertical.rows() == rows-1);
    assert(weights_vertical.cols() == cols);

    Eigen::Vector2i dims(rows, cols);

    auto isSeedPoint = [&] (Eigen::Vector2i pos) {
        return labels(pos(0), pos(1))[0] > 0;
    };

    std::vector<size_t> imgToMatTable;
    size_t img_size = rows*cols;
    imgToMatTable.reserve(img_size);
    size_t labeledIndex = 0;
    size_t unlabeledIndex = 0;
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Eigen::Vector2i pos(y,x);
            size_t i = toLinear(dims, pos);
            if(isSeedPoint(pos)) {
                imgToMatTable[i] = labeledIndex;
                ++labeledIndex;
            } else {
                imgToMatTable[i] = unlabeledIndex;
                ++unlabeledIndex;
            }
        }
    }
    size_t unlabeled = unlabeledIndex;
    size_t labeled = labeledIndex;
    assert(labeled + unlabeled == img_size);

    Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic> xm = Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic>::Zero(labeled, num_classes);

    std::vector<Eigen::Triplet<element_type>> triplets_lu;
    std::vector<Eigen::Triplet<element_type>> triplets_bt;

    const Image<float, 1>* weight_images[] = {&weights_vertical, &weights_horizontal};

    std::vector<float> diagonal(unlabeled, 0.0f);
    for(int d = 0; d < 2; ++d) {

        Eigen::Vector2i start(0,0);
        start(d) = 1;
        auto& weights = *weight_images[d];
        for(int y = start(0); y < rows; ++y) {
            for(int x = start(1); x < cols; ++x) {

                Eigen::Vector2i pos(y,x);
                //float v1 = img(pos(0), pos(1));
                int lp = toLinear(dims, pos);
                size_t i1 = imgToMatTable[lp];

                bool currentIsSeedPoint = isSeedPoint(pos);

                auto neigh = pos;
                neigh[d] -= 1;

                //float v2 = img(neigh(0), neigh(1));
                float w = weights(neigh(0), neigh(1))[0];

                assert(std::isfinite(w) && !std::isnan(w));
                w += 0.00001f;

                int ln = toLinear(dims, neigh);
                size_t i2 = imgToMatTable[ln];
                if(isSeedPoint(neigh)) {
                    if(!currentIsSeedPoint) {
                        //unlabeled left, labeled right
                        triplets_bt.emplace_back(i1,i2,w);
                    } //else case is not interesting, as we are not interested in matrix lm
                } else {
                    diagonal[i2] += w;
                    if(currentIsSeedPoint){
                        //unlabeled left, labeled right
                        triplets_bt.emplace_back(i2,i1,w);
                    } else {
                        //std::cout << "p1 " << pos << std::endl;
                        //std::cout << "p2 " << neigh << std::endl;
                        //std::cout << "i1 " << i1 << std::endl;
                        //std::cout << "i2 " << i2 << std::endl;
                        triplets_lu.emplace_back(i1,i2,-w);
                        triplets_lu.emplace_back(i2,i1,-w);
                    }
                }
                if(!currentIsSeedPoint) {
                    diagonal[i1] += w;
                }
            }
        }
    }
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            Eigen::Vector2i pos(y,x);
            bool currentIsSeedPoint = isSeedPoint(pos);
            int lp = toLinear(dims, pos);
            size_t i1 = imgToMatTable[lp];
            if(currentIsSeedPoint) {
                size_t cls = labels(pos(0),pos(1))[0];
                xm(i1, cls-1) = 1.0f;
            }
        }
    }

    for(int i=0; i<unlabeled; ++i) {
        triplets_lu.emplace_back(i,i,diagonal[i]);
    }

    Eigen::SparseMatrix<element_type, Eigen::ColMajor> lu(unlabeled,unlabeled);
    lu.reserve(5); // Reserve 5 elements per row/col

    lu.setFromTriplets(triplets_lu.begin(), triplets_lu.end());

    lu.makeCompressed();

    Eigen::SparseMatrix<element_type> bt(unlabeled,labeled);
    bt.setFromTriplets(triplets_bt.begin(), triplets_bt.end());

    Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> btms = bt * xm;

#if defined(USE_MAGMA)
    magma_queue_t queue;
    int device;
    magma_getdevice(&device);
    magma_queue_create(device, &queue);

    magma_d_matrix lu_d, btms_d;
    magma_d_matrix lu_m = eigen_to_magma_sparse(lu, queue);
    CHECK_MAGMA_ERROR(magma_d_vtransfer(lu_m, &lu_d, Magma_CPU, Magma_DEV, queue));

    Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> res_x(btms.rows(), btms.cols());

    for(int c = 0; c < num_classes; ++c) {
        magma_d_matrix btms_m, btms_d;

        int vec_cols = 1;
        int rows = btms.rows();
        double* data = &btms.data()[c*rows];
        CHECK_MAGMA_ERROR(magma_dvset(rows, vec_cols, data, &btms_m, queue));

        CHECK_MAGMA_ERROR(magma_d_mtransfer(btms_m, &btms_d, Magma_CPU, Magma_DEV, queue));

        magma_d_matrix res_d;
        CHECK_MAGMA_ERROR(magma_d_vinit(&res_d, Magma_DEV, btms.rows(), vec_cols, 1.0/num_classes, queue));

        magma_dopts dopts;

        dopts.solver_par.solver = Magma_PCGMERGE;
        dopts.solver_par.rtol = 1e-10;
        dopts.solver_par.maxiter = 1000;
        dopts.solver_par.verbose = 0;
        CHECK_MAGMA_ERROR(magma_dsolverinfo_init(&dopts.solver_par, &dopts.precond_par, queue));

        dopts.precond_par.solver = Magma_JACOBI;
        CHECK_MAGMA_ERROR(magma_d_precondsetup(lu_m, btms_m, &dopts.solver_par, &dopts.precond_par, queue));

        CHECK_MAGMA_ERROR(magma_d_solver(lu_d, btms_d, &res_d, &dopts, queue ));

        magma_d_matrix res_m;
        CHECK_MAGMA_ERROR(magma_d_mtransfer(res_d, &res_m, Magma_DEV, Magma_CPU, queue));

        magma_int_t res_rows, res_cols;
        double* res_data;
        CHECK_MAGMA_ERROR(magma_dvget(res_m, &res_rows, &res_cols, &res_data, queue));
        assert(res_cols == vec_cols);

        double* res_x_data = &res_x.data()[c*rows];
        std::copy_n(res_data, res_rows, res_x_data);

        CHECK_MAGMA_ERROR(magma_dsolverinfo_free(&dopts.solver_par, &dopts.precond_par, queue));
        CHECK_MAGMA_ERROR(magma_d_mfree(&btms_m, queue));
        CHECK_MAGMA_ERROR(magma_d_mfree(&btms_d, queue));
        CHECK_MAGMA_ERROR(magma_d_mfree(&res_m, queue));
        CHECK_MAGMA_ERROR(magma_d_mfree(&res_d, queue));
    }

    CHECK_MAGMA_ERROR(magma_d_mfree(&lu_m, queue));
    CHECK_MAGMA_ERROR(magma_d_mfree(&lu_d, queue));

    magma_queue_destroy( queue );
    //magma_finalize();

#else
#if 1
    Eigen::SimplicialLDLT<Eigen::SparseMatrix<element_type, Eigen::ColMajor>> solver;
    solver.analyzePattern(lu);
    solver.factorize(lu);

    Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic> res_x = solver.solve(btms);
#else
    Eigen::ConjugateGradient<Eigen::SparseMatrix<element_type>, Eigen::Lower|Eigen::Upper> solver;
    //solver.setTolerance(1e-3);
    solver.compute(lu);

    element_type init_val = 1.0f/num_classes;
    auto initialization = init_val * Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic>::Ones(unlabeled, num_classes);

    Eigen::Matrix<element_type, Eigen::Dynamic, Eigen::Dynamic> res_x = solver.solveWithGuess(btms, initialization);
    //std::cout << "#iterations:     " << solver.iterations() << std::endl;
    //std::cout << "estimated error: " << solver.error()      << std::endl;
#endif
#endif

    std::vector<Image<float, 1>> results;

    for(int output_label = 1; output_label <= num_classes; ++ output_label) {
        Image<float, 1> output(rows, cols);
        for(int y = 0; y < rows; ++y) {
            for(int x = 0; x < cols; ++x) {
                Eigen::Vector2i pos(y,x);
                int l = toLinear(dims, pos);

                float val;
                size_t label = labels(pos(0), pos(1))[0];
                if(label != 0) {
                    val = (label == output_label) ? 1.0f : 0.0f;
                } else {
                    size_t i1 = imgToMatTable[l];
                    val = res_x(i1, output_label-1);
                }
                output(pos(0), pos(1)) = Pixel<float, 1>(val);
            }
        }

        results.push_back(std::move(output));
    }

    Image<uint32_t, 1> classes(rows, cols);
    for(int y = 0; y < rows; ++y) {
        for(int x = 0; x < cols; ++x) {
            int best = -1;
            float best_prob = -std::numeric_limits<float>::infinity();
            int i=1;
            for(auto& result : results) {
                float res = result(y,x)[0];
                if(res >= best_prob) {
                    best = i;
                    best_prob = res;
                }
                i+=1;
            }
            classes(y,x) = Pixel<uint32_t, 1>(best);
        }
    }
    return {classes, results};
}

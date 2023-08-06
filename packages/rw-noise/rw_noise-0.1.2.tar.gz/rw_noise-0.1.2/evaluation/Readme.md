# Scripts used for evaluation of RW weight functions

The scripts contained in this folder and described in this document were used for the experiments conducted in the following publication:
```
A Bhattacharyya Coefficient-Based Framework for Noise Model-Aware Random Walker Image Segmentation
Dominik Drees, Florian Eilers, Ang Bian and Xiaoyi Jiang
```
If you use this code in your research, please cite the above as a reference.

In total, three experiments were conducted (on synthetic data, on FIM images of larvae and on MRI data from the FastMRI dataset) which are described in sections below.

# Preparations

First, build and install the python package in the root of the repository as described in the the file [Readme.md](../Readme.md) there.

For the real world data evaluation, you also need to download the [FIM and FastMRI data](https://uni-muenster.sciebo.de/s/DK9F0f6p5ppsWXC).

# Synthetic data (folder `spiral`)

This experiment aims to demonstrate the seed propagation capabilities of different weight functions under different noise conditions.
As the images are generated in the scripts themselves, no further configuration is necessary.
You can:
 * Execute `illustration.py` to generate the illustrative figures in the paper.
 * Execute `run_evaluation.py` to generate a file `result.csv` which contains the quantitative results reported in the paper.

# FIM larvae images (folder `fim`)

This experiments aims to demonstrate the performance of different weight functions in an environment dominated by Poisson noise.
You likely have to change the data path in `data.py` to point to the folder containing the `*.npy` and `*_mask.npy` files.

You can:
 * Execute `illustration.py` to generate the illustrative figures in the paper.
 * Execute `run_evaluation.py` to generate a file `result.csv` which contains the quantitative results reported in the paper.

# FastMRI knee images (folder `fastmri`)

This experiments aims to demonstrate the performance of different weight functions in an environment dominated by two dimensional gaussian noise.
You likely have to change the data path in `data.py` to point to the folder containing the `*.npy` and `*_mask.npy` files.
Note: Due to restrictions imposed by the creators of the FastMRI dataset, we are unable redistribute the reconstructed mri files directly.
To reproduce our results you will have to:
1) Obtain a copy of the original [FastMRI dataset](https://fastmri.med.nyu.edu/).
2) Reconstruct the image volumes from the given kspace data using (for example) slicewise the `numpy.fft.ifft2` function.
3) Extract slices matching to the mask files provided by us (see link above).
The file name structure of the mask files is `<fastmri_dataset_name>_<slice_number>_mask.npy` (e.g., `file1000000_15_mask.npy`), so you will have to convert `<fastmri_dataset_name>.h5` (e.g., `file1000000.h5`), extract and reconstruct slice `<slice_number>` and save it as `<fastmri_dataset_name>_<slice_number>.npy` (e.g., `file1000000_15.npy`).

You can:
 * Execute `illustration.py` to generate the illustrative figures in the paper.
 * Execute `run_evaluation.py` to generate a file `result.csv` which contains the quantitative results reported in the paper.
 * Execute `interactive_segmentation.py` to interactively use RW and weight functions (F1-F7) to segment FastMRI images.


# Plotting Quantitative Results

You can use the script `plot_results.py` to generate the plots of quantitative results also shown in the paper.
The script assumes that the respective `result.csv` reside in the folders `spiral`, `fim` and `fastmri`.
This happens automatically if you execute the `run_evaluation.py` scripts within those directories.
You can then just execute the script `plot_results.py` and optionally add a path to a folder as an argument to export the figures to files.

# Note! Updates since the publication of the original paper

Since the publication, an error in the calculation of region variances has been noticed and fixed. The results produced with versions `>= 0.1.2` will thus not reflect the paper results exactly.

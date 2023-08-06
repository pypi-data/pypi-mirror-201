from cmake_build_extension import BuildExtension, CMakeExtension
from setuptools import setup

with open("__init__.py", "r") as f:
    init_py = f.read()

setup(
    ext_modules=[
        CMakeExtension(
            name="rw_noise",
            install_prefix="rw_noise",
            write_top_level_init=init_py,
            #cmake_depends_on=["boost", "openmp"],
            cmake_depends_on=[],
            disable_editable=True,
            cmake_configure_options=[
                '-DUSE_MAGMA:BOOL=OFF',
            ],
        )
    ],
    cmdclass=dict(build_ext=BuildExtension),
)

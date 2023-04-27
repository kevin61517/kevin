from distutils.core import setup
from Cython.Build import cythonize

if __name__ == '__main__':
    setup(
        name='aaa/cython_test',
        ext_modules=cythonize(["*.pyx"]),
    )

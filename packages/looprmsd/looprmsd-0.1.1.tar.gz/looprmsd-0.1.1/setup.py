from setuptools import setup, find_packages

setup(
    name='looprmsd',
    version='0.1.1',
    author='Jeffrey Lim',
    author_email='js.lim@galux.co.kr',
    description='LoopRMSD is a Python package for calculating the RMSD of a loop region given two pdbs',
    # packages=find_packages(),
    py_modules=['loop_rmsd_antibody'],
    install_requires=[
        'numpy',
        'biopython'
    ],
)
from setuptools import setup, find_packages

setup(
    name='looprmsd',
    version='0.1.5',
    author='Jeffrey Lim',
    author_email='js.lim@galux.co.kr',
    description='LoopRMSD is a Python package for calculating the RMSD of a loop region given two pdbs',
    # py_modules=['loop_rmsd_antibody'],
    packages=find_packages(),
    package_data={'looprmsd': ['dat/*.pdb']},
    install_requires=[
        'numpy',
    ],
)
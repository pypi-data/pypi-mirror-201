from distutils.core import setup
from pathlib import Path

def get_install_requires():
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setup(
    name='zliPkg1',
    version='11.31',
    license='MIT',
    author='zli',
    packages=['zliPkg'],
    package_dir={'zliPkg': 'zliPkg'},
    install_requires=get_install_requires()
)

from setuptools import find_packages, setup

import jcs_mediagraphic


install_requires = [
    "pip",
    "fpdf2",
    "Pillow"
]




def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name='jcs_mediagraphic',
    version=jcs_mediagraphic.__version__,
    description='Python library for MediaGraphic Group usages',
    author=jcs_mediagraphic.__author__,
    license=jcs_mediagraphic.__license__,
    packages=find_packages(include=['jcs_mediagraphic']),
    install_requires=install_requires,
)
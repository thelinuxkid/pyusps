#!/usr/bin/python
from setuptools import setup, find_packages
import os

EXTRAS_REQUIRES = dict(
    test=[
        'fudge>=1.0.3',
        'nose>=1.1.2',
        ],
    dev=[
        'ipython>=0.12.1',
        ],
    )

# Pypi package documentation
root = os.path.dirname(__file__)
path = os.path.join(root, 'README.rst')
with open(path) as fp:
    long_description = fp.read()

setup(
    name='pyusps',
    version='0.0.5',
    description='pyusps -- Python bindings for the USPS Ecommerce APIs',
    long_description=long_description,
    author='Andres Buritica',
    author_email='andres@thelinuxkid.com',
    maintainer='Andres Buritica',
    maintainer_email='andres@thelinuxkid.com',
    url='https://github.com/thelinuxkid/pyusps',
    license='MIT',
    packages = find_packages(),
    namespace_packages = ['pyusps'],
    test_suite='nose.collector',
    install_requires=[
        'setuptools>=0.6c11',
        'lxml>=2.3.3',
        'ordereddict==1.1',
        ],
    extras_require=EXTRAS_REQUIRES,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
)

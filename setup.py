#!/usr/bin/python
from setuptools import setup, find_packages

EXTRAS_REQUIRES = dict(
    # Using tests_require to specify test dependencies fails.
    # https://groups.google.com/forum/#!topic/nose-users/fnJ-kAUbYHQ
    test=[
        'fudge>=1.0.3',
        'nose>=1.1.2',
        ],
    dev=[
        'ipython>=0.12.1',
        ],
    )

setup(
    name='pyusps',
    version='0.0.2',
    description='pyusps -- Python bindings for the USPS Ecommerce APIs',
    long_description='Python bindings for the USPS Ecommerce APIs',
    license='GPL',
    author='Andres Buritica',
    author_email='andres@thelinuxkid.com',
    maintainer='Andres Buritica',
    maintainer_email='andres@thelinuxkid.com',
    url='https://github.com/andresburitica/pyusps',
    packages = find_packages(),
    namespace_packages = ['pyusps'],
    test_suite='nose.collector',
    install_requires=[
        'setuptools>=0.6c11',
        'lxml>=2.3.3',
        'ordereddict==1.1',
        ],
    extras_require=EXTRAS_REQUIRES,
    )

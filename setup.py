import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='scidash-api',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Scidash Client library for uploading data',
    long_description=README,
    url='https://github.com/MetaCell/scidash-api',
    author='MetaCell',
    author_email='info@metacell.us',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'cerberus==1.1',
        'dpath==1.4.2',
        'requests==2.18.4',
        'six==1.11.0'
    ]
)

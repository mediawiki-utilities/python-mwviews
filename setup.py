import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name='mwviews',
    version='0.0.3',
    author='Dan Andreescu',
    author_email='dandreescu@wikimedia.org',
    description='Tools for parsing and querying Wikimedia Foundation' +
                ' pageview data, from both static dumps and online API',
    license='MIT',
    url='https://github.com/mediawiki-utilities/python-mwviews',
    download_url='https://github.com/mediawiki-utilities/python-mwviews/tarball/0.0.1',
    packages=find_packages(),
    keywords=['wikimedia', 'wikipedia', 'pageview', 'api'],
    install_requires=['requests', 'futures']
)

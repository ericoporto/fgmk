# -*- coding: utf-8 -*-
from setuptools import setup
from codecs import open
import platform
import errno
import sys
import os
import re
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

def mkdir_p(path):
#thanks http://stackoverflow.com/a/600612/965638
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

datafiles = dict(data_files=[])
osname = platform.system()
if osname == 'Linux':
    linuxdist = platform.linux_distribution()[0]
    if linuxdist == 'Ubuntu' or linuxdist =='Debian':
        mkdir_p(os.path.expanduser('~/.local/share/applications'))
        mkdir_p(os.path.expanduser('~/.local/share/icons'))
        mkdir_p(os.path.expanduser('~/.local/share/mime'))
        datafiles = dict(data_files=[('share/applications', ['platform/ubuntu/fgmk.desktop']),
                    ('share/icons', ['platform/ubuntu/fgmk.svg',
                                          'platform/ubuntu/fgmk-map.svg']),
                    ('share/mime', ['platform/ubuntu/fgmk.xml'])])

with open('fgmk/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

test_requirements = ['pytest>=2.8.0']

if(int(sys.version_info.major) == 2):
    install_requires = ['numpy','pillow']
    print("!!!Please INSTALL PYQT5!!!")
else:
    install_requires = ['numpy','pillow','pyqt5']

setup(
    name='fgmk',
    version=version,
    description='A PyQt5 Maker to generate a RPG Javascript game.',
    long_description=long_description,
    url='https://github.com/ericoporto/fgmk',
    download_url = 'https://github.com/ericoporto/fgmk/tarball/'+version,
    author='Erico Vieira Porto',
    author_email='ericoporto2008@gmail.com',
    license='GPLv2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    keywords='game development',
    install_requires=install_requires,
    packages = ["fgmk","fgmk.ff","fgmk.util","fgmk.dock"],
    entry_points={
        'gui_scripts': [
            'fgmk = fgmk.__main__:main'
            ]
    },
    package_data = {
        'fgmk': ['data/*.png',
                 'data/actions/*.png',
                 'data/*.json',
                 'data/basegame.tar.gz',
                 'data/example.tar.gz',
                 'data/fgmk.qhc',
                 'data/fgmk.qch']
    },
    **datafiles
)

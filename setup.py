from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fgmk',
    version='1.0.0',
    description='A PyQt5 Maker to generate a RPG Javascript game.',
    url='https://github.com/ericoporto/fangamk',
    author='Erico Vieira Porto',
    author_email='elhafulvics@gmail.com',
    license='GPLv2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='game development',
    install_requires=['numpy','pillow','pyqt5'],
    packages = ["fgmk"],
    package_dir = {"": "src"},
    scripts = ["fgmk"],
    package_data = {
        'fgmk': ['data/*.png','data/*.json','data/basegame.tar.gz']
    }
)

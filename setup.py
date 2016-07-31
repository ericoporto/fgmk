from setuptools import setup
from codecs import open
import platform
import errno
import os

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
        datafiles = dict(data_files=[('share/applications', ['src/platform/ubuntu/fgmk.desktop']),
                    ('share/icons', ['src/platform/ubuntu/fgmk.svg',
                                          'src/platform/ubuntu/fgmk-map.svg']),
                    ('share/mime', ['src/platform/ubuntu/fgmk.xml'])])



setup(
    name='fgmk',
    version='0.2.2',
    description='A PyQt5 Maker to generate a RPG Javascript game.',
    url='https://github.com/ericoporto/fgmk',
    download_url = 'https://github.com/ericoporto/fgmk/tarball/0.2.2',
    author='Erico Porto',
    author_email='elhafulvics@gmail.com',
    license='GPLv2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='game development',
    install_requires=['numpy','pillow','pyqt5'],
    packages = ["fgmk"],
    package_dir = {"": "src"},
    entry_points={
        'gui_scripts': [
            'fgmk = fgmk.__main__:main'
            ]
    },
    package_data = {
        'fgmk': ['data/*.png','data/*.json','data/basegame.tar.gz']
    },
    **datafiles
)

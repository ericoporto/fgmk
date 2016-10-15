#!/bin/bash
# this script is temporary until I learn ReStructured Text
# optionally this script should be converted to python for better portability.

mkdir -p build

#clean directory
rm -rf Rst
rm -rf source/index.rst
rm -rf source/conf.py
rm -rf source/Installation
rm -rf source/Editor
rm -rf source/Actions
rm -rf source/EditorCode
rm -rf source/Future
rm -rf source/Quickstart
rm -rf source/Roadmap
rm -rf source/Specification
rm -rf build/*

# using copy with cp is a bad idea. It can corrupt files.
# alternatively, I am using rsync.
# TODO: rewrite the copy safely with Python.


#a brand new from the Markdown
rsync -a Markdown/ Rst

#lets convert everything to RestructuredText
python3 recursiveMd2Rst.py

#lets make all links correct
cd Rst
 find . -type f -iname "*.rst" -exec sed -i 's/\.md/\.html/g' {} \;

#lets go back
cd ..

rsync -a Rst/Installation/ source/Installation
rsync -a Rst/Actions/ source/Actions
rsync -a Rst/Editor/ source/Editor
#rsync -a Rst/EditorCode/ source/EditorCode
#rsync -a Rst/Future/ source/Future
rsync -a Rst/Quickstart/ source/Quickstart
#rsync -a Rst/Roadmap/ source/Roadmap
rsync -a Rst/Specification/ source/Specification

rsync -a index_qthelp.rst source/index.rst
rsync -a conf_qthelp.py source/conf.py

make qthelp
/usr/lib/x86_64-linux-gnu/qt5/bin/qcollectiongenerator build/qthelp/fgmk.qhcp
rsync build/qthelp/fgmk.qhc ../fgmk/data/fgmk.qhc
rsync build/qthelp/fgmk.qch ../fgmk/data/fgmk.qch

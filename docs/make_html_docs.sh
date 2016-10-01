#!/bin/bash
mkdir -p build

#clean directory
rm -rf Rst
rm -rf source/Editor
rm -rf source/Actions
rm -rf source/EditorCode
rm -rf source/Future
rm -rf source/Quickstart
rm -rf source/Roadmap
rm -rf source/Specification

#a brand new from the Markdown
cp -rf Markdown Rst

#lets convert everything to RestructuredText
python3 recursiveMd2Rst.py

#lets make all links correct
cd Rst
find . \( ! -regex '.*/\..*' \) -type f -print0 | xargs -0 sed -i 's/.md/.html/g'

#lets go back
cd ..

cp -rf Rst/Actions source/Actions
cp -rf Rst/Editor source/Editor
cp -rf Rst/EditorCode source/EditorCode
cp -rf Rst/Future source/Future
cp -rf Rst/Quickstart source/Quickstart
cp -rf Rst/Roadmap source/Roadmap
cp -rf Rst/Specification source/Specification

cp index.rst source/index.rst

rm -rf build/*

make html

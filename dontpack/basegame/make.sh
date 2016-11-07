#!/bin/bash

# get the latest release of the engine
curl -s -L https://github.com/ericoporto/fgmkJsEngine/releases/latest | 
    egrep -o '/ericoporto/fgmkJsEngine/releases/download/[.0-9]+/index.html' | 
    wget --base=http://github.com/ -i - -O index.html

# pack everything 
tar -czvf basegame.tar.gz audio/ descriptors/ img/ icon.png index.html LICENSE

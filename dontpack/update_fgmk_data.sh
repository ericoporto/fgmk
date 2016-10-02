#!/bin/bash

cd example
./make.sh
cd ../basegame
./make.sh
cd ..
rsync example/example.tar.gz ../fgmk/data/example.tar.gz
rsync basegame/basegame.tar.gz ../fgmk/data/basegame.tar.gz

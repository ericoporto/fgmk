![Icon](iconTiny.png) Contributing to fgmk
==========================================

I am very happy you are interested in contributing!!!
There are several ways one could contribute to the fgmk project. This guide
should help you getting started.

## Table of Contents

[Introduction](#introduction)

[Documentation](#documentation)

[Coding](#coding)

[Assets](#assets)

[Testing](#testing)

[BugHunting](#bughunting)


## Introduction

The fgmk project is a small project, it's composed of this repository, which
is the Game Editor, and some additional ones:

- [fgmkJsEngine](https://github.com/ericoporto/fgmkJsEngine): this is a
javascript engine, it can be contained in a single `index.html` file that can
be dropped in the game folder and run the game files.
- [fgmkPackaging](https://github.com/ericoporto/fgmkPackaging): this repository
deals with packaging the interface (outside of PyPI) and in the future also the
games - as electron apps, or whatever new ways may be present.
- [fangamk](https://github.com/ericoporto/fangamk): historical repository, right
now hosts some [experimental code](https://github.com/ericoporto/fangamk/tree/master/GameMusic)
and [documentation](https://github.com/ericoporto/fangamk/tree/master/Descriptor).
This repository is probably going away.

The focus of this project is being able to make a game, in a way that the hard
parts are abstracted first in the editor, then in the engine and last in the
assets - including the descriptor files. Also the descriptor files should be
easy to open in a text editor so you can understand the logic the engine is
playing.

It should be easy enough that a child should be able to open and modify a text
file and see the change in the game without breaking it - so the formatting
of the descriptor files should be intuitive.

Last but not least, the editor should be accompanied by an interesting and small
game, so one could play, and understand the game logic by copying from this
game.

## Documentation

There is some documentation floating around, but this is a important part of the
project, if you want to help me getting things out of my head, mail me - you can
find my email in the [setup.py](https://github.com/ericoporto/fgmk/blob/master/setup.py).

## Coding

The code is currently very rushed together, it could be improved a lot.

If you are adding a feature to the engine, so it can be reused for several
games, reflect about the minimum customization that feature could have. Adding
a feature to the engine will imply knowing how to modify the jsons so it can
be accessed, if needed, and in this case it will imply in changing the editor so
it can generate cohesive json files, and also being able to open and edit them.

## Assets

Currently the editor is very bad at handling a large assets library. This is
because it's not a problem right now. If you want to make this a problem - and
I would be very happy with this problem - please consider contributing assets to
the project. The assets can be png images, sound effects or music. Right now the
engine doesn't support music, but probably will in the future.

The game uses 32x64 pixel images for the sprites of the characters and 32x32
pixel for each tile in the game map. I suggest you explore the existing images
and keep the style compatible.

**Don't rip existing game images**, only original content that can be made
available with a permissive license should be submitted. This asset also won't
be accepted right a way, since once a great number of assets exist that will
demand having a place to store and download them.

## Testing

for human testing see [BugHunting](#bughunting).

The interface could use some automated testing, if you want to help writing
tests, this would be awesome!

The tests should be able to run by typing

    python3 setup.py test

    # note: in your system the python 3 executable may be named just python

## BugHunting

If you have time to do help catch some usability bugs, please use the project
and submit your thoughts through the [issues page](https://github.com/ericoporto/fgmk/issues).

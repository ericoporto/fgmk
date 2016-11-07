# Specification

The engine and the editor expects some files, and that they are organized in the
following manner.

Here is how the file tree should be  organized

    game_project_name
    ├── audio
    │   └── music
    ├── descriptors
    │   ├── charaset
    │   │   └── charaset1.json
    │   ├── charas.json
    │   ├── feedback.json
    │   ├── hms.json
    │   ├── init.json
    │   ├── items.json
    │   └── levels
    │       ├── ahouse.map.json
    │       └── house.pal.json
    |        ...
    ├── icon.png
    ├── img
    │   ├── bgimg1.png
    │   ├── charaset.png
    │   ├── faceset.png
    │   ├── monsterset.png
    │   ├── pictures
    │   │   └── example.png
    |   |    ...
    │   ├── printer.png
    │   ├── sys
    │   │   ├── controllers.png
    │   │   ├── keys0.png
    │   │   ├── keysexplainer.png
    │   │   └── pckeys.png
    │   ├── tile.png
    │   └── title.png
    └── index.html


- `audio` (folder) - contains audio files used by the game.

    - `music` (folder) - this folder contains the music. A music file can be either .mp3,
    .ogg or .wav. You can add music files with the same name and different extensions to
    maximize browser compatibility. When downloading, the engine will prefer ogg first (if 
    the browser supports it), then mp3 and later wav.

- `descriptors` (folder) - contains all json files, and folders containing json
files.

    - `charaset` (folder) - this folder contains the different jsons that describes the
    animations you use with Charas.

    OBS: right now only a single file that has to be named `charaset1.json` is
    possible. Soon this won't be a requirement.

    - `charas.json` - things that you can place in any the map, they can move and
    trigger actions, and usually represent the non playable characters you interact
    in the game.

    - `feedback.json` - deals with the engine feedback, right now only colision and
    the sound when outputing text. This should be moved inside the engine soon.

    - `hms.json` - Heroes, Monsters and Skills, this file describes all the heroes
    that you can add to the party, all the monsters you can fight against, and the
    skills that they can have.

    - `init.json` - where does the game starts, who is in the party, and some things
    that didn't fit anywhere else.

    - `items.json` - has the description of the items, how do they work, what they
    are.

    - `scriptedbattles.json` - has the description of a scripted battle, what
    monsters are involved and how each script is triggered.

    - `levels` (folder) - this folder contains levels (.map.json files) and possible
    palettes (.pal.json files) to use when designing levels.


- `img` (folder) - this folder contains all the image files in png format.

    - `pictures` (folder) - you can show a picture using action, this folder
    contains possible pictures in png format.

- `index.html` - this is the engine. It should be placed at the root of the
game project folder.


## palette files - .pal.json

A palette specifies how an image is going to be sliced in tiles to be available
for drawing maps. An image can be like below - note, the first 32x32 pixel tile
should always be empty.

![](tile4x.png)

This file holds a palette of tiles, it's used to "paint" maps, each tile in a
map layer (1,2 and 4) will be translated to a cropped piece of 32 pixels in width
and height from the image.

    {
        "tilesAnimated":
        {
            "8":
                 [[  0, 2],
                  [  1, 2],
                  [  2, 2],
                  [  3, 2]] },
        "tiles":
        {   "1":  [  1, 0],
            "2":  [  2, 0],
            "3":  [  3, 0],
            "4":  [  0, 1],
            "5":  [  1, 1],
            "6":  [  2, 1],
            "7":  [  3, 1],
            "8":  [  1, 2]  },
        "tileImage": "img/tile.png"
    }

![](tile4x_marks.png)

*the image above represents the palette*

- `tileImage` : the relative path to a png image that is used by the palette.

- `tiles` : this contains a dictionary of numbers, and each number points to a
32x32 pixel piece of the image pointed by `tileImage`.
    - `tiles: "1" : [X,Y], "2" : [X,Y], ...`

- `tilesAnimated` : this contains a dictionary of numbers, and each number points
to a list that points a different 32x32 pixel piece of the image pointed by
`tileImage`, describing an animated tile.


## map files - .map.json

Below is an example file with each field that is expected to be available. Each
numeric 2d matrix is of the same size, which is defined as map width and height.
The matrix is described as a list (y dimension) of lists (x dimension). In a
4 x 3 fictious map, this matrix would be something like:

    "layer:"
        [[ 0, 0, 0, 0],
         [ 0, 0, 0, 0],
         [ 0, 0, 0, 0]]

You can think of a map as having for layers, the **first** layer, named `layer1`
is drawn first, and **second** the `layer2` is drawn next, the `player` and
`charas` are drawn in the **third** layer where the `colision` takes place to,
and on top the fourth layer, `layer4`, is drawn.

    { "Level":
        { "charas":  [],
          "colision":
                [[]],
          "events":
                [[]],
          "eventsActions":
              { "1":
                  [["ACTIONNAME","PARAM1;PARAM2;..."],
                   ["ACTIONNAME","PARAM1;PARAM2;..."]],
                "2":
                  [["ACTIONNAME","PARAM1;PARAM2;..."]] },
          "eventsType":
              { "1":  [  1,  0],
                "2":  [  1,  0]},
          "layer1":
              [[]],
          "layer2":
              [[]],
          "layer4":
              [[]],
          "levelName": "very_simple_map",
          "tileImage": "img/tile.png",
          "tiles":
              { "1":  [ 11, 12],
                "2":  [  1,  1] },
          "tilesAnimated":
              { }
        }
    }

Each `.map.json` file has the keywork `Level` at top-level.

- `charas` : a list of the charas that should be placed in the map
and their x and y position.
  - `"charas": [["CHARANAME",X,Y],["CHARANAME",X,Y],...]` .

  - Example: `"charas": [["bear",12,7]]`

- `colision` : a 2d numeric matrix, where 0 represents floor and 1 represents
walls.

- `events` : a 2d numeric matrix, where 0 represents no event, and any other
number represents an event.

- `eventsActions` : a dictionary where each event is represented by a number and
each number contains a list of actions and parameters.

  - `"eventsActions": { "1":[["ACTIONNAME","PARAM1"], ["ACTIONNAME","PARAM1;PARAM2"]] }`

- `eventsType` : a dictionary where each event is represented by a number and
each number contains an array representing when the event is triggered.

    - possible triggers are:

        - onclick : means the event is triggered when the player is adjacent to the tile, and presses the interaction button.

            - this is represented by the list `[1,0]`

        - ontouch : means the event is triggered when the player character is on the same tile.

            - this is represented by the list `[0,1]`

        - ideally a simple list that could contain the `onclick` and `ontouch` words would be clearer.

- `layer1` : a 2d numeric matrix, where 0 represents a clear tile, and any other
number represents a tile that is going to be drawn.

- `layer2` : a 2d numeric matrix, where 0 represents a clear tile, and any other
number represents a tile that is going to be drawn.

- `layer4` : a 2d numeric matrix, where 0 represents a clear tile, and any other
number represents a tile that is going to be drawn on top of the first, second
and third layer.

- `levelName` : the name of the map.

  - Right now this needs to be the same as the map file name without the .map.json .

- `tileImage` : the relative path to a png image that is used by the palette.

- `tiles` : this contains a dictionary of numbers, and each number points to a
32x32 pixel piece of the image pointed by `tileImage`.
    - `tiles: "1" : [X,Y], "2" : [X,Y], ...`

- `tilesAnimated` : this contains a dictionary of numbers, and each number points
to a list that points a different 32x32 pixel piece of the image pointed by
`tileImage`, describing an animated tile.

## init.json

The `init.json` file is the first json file that the game engine should read.
It contains information on what's needed to successfully start the engine, being
the most notable, the initial information about the player chara - the chara the
person playing the game controls and uses to interact with the maps.

It's important to notice that *javascript* can't look for any files in a
directory in a webserver from the client side, it must previously know the full
name of the files. So some minimal information about the files to expect are
available here too.

Below is an example of a `init.json` file. Note that the engine will look for
this exact name and case matters, so the file must be named `init.json`, and
placed inside the `game_root_folder/descriptors/` folder.

    {
        "CharasFileList": {
            "charas1": "charas1.json"
        },
        "CharasetFileList": {
            "charaset1": "charaset1.json"
        },
        "MusicList":{
            "villa" : {"ogg":"villa.ogg","mp3":"villa.mp3"},
            "battle_1": {"ogg":"battle_1.ogg","mp3":"battle_1.mp3"},
            "battle_win": {"ogg":"battle_win.ogg","mp3":"battle_win.mp3"},
            "opening": {"ogg": "opening.ogg","mp3": "opening.mp3"}
        },
        "HMSFile": "hms.json",
        "LevelsList": {
            "ahouse": "ahouse.map.json"
        },
        "PictureList":["test"]
        ,
        "Player": {
            "charaSet": "person",
            "facing": "down",
            "initPosX": 224,
            "initPosY": 224,
            "party": [
                "hero"
            ]
        },
        "World": {
            "initLevel": "ahouse"
            "initMusic": "opening",
            "battleMusic": "battle_1",
            "battleVictoryMusic": "battle_win",
            "initActions": [["playMusic","villa"]]
        },
        "itemsFile": "items.json"
    }

***note:*** all path in this file is relative to the root of the `descriptors`
folder.

- `CharasFileList` : points to a list of `chara` files, where each key is the name
of the file minus it's extension.

- `CharasetFileList` : points to a list of `charaset` files, where each key is the
name of the file minus it's extension.

- `MusicList` : contains the music names and the file for each extension available
in audio/music folder.

- `HMSFile` : points to where to look for the Heroes Monsters Skills file and
it's name. It's advised to keep this value as `hms.json` to avoid confusion.

- `LevelsList` : points to a list of map (`.map.json`) files, where each key is
the name of the file minus it's extension.

- `PictureList` : points to a list of pictures, minus extension. These files
should be png files, placed in the `game_root_folder/img/pictures/` for the
engine to find these files. This is the only path not relative to the
descriptors folder in the `init.json` file.

- `itemsFile` : "items.json"

- `Player` : describes the initial states of the player chara when the engine is
the first time in the map state.

    - `charaSet` : the name of the charaset used by the player chara.

    - `facing` : which direction the player chara will be facing, can be either `up`,`down`,`left` or `right`.

    - `initPosX` : at what x (horizontal) position in the map should the player chara start.

    - `initPosY` : at what y (vertical) position in the map should the player chara start.

    - `party` : a list containing the key names of the Heroes in the starting party - this only matters for battle.

- `World`: describes the initial states of the environment.

    - `initLevel` : the key name of the level the player chara begins. This is the first map you see after the start screen.
    
    - `initMusic` : the name of the music in the opening screen.
    
    - `battleMusic` : the name of the default music to play in battle if no music is specified.
    
    - `battleVictoryMusic` : the name of the default music to play when the battle ends in victory if no music is specified.
    
    - `initActions` : in the opening screen, when start is clicked, these actions should be executed.

## items.json

The file that describes items, all items here can be added to the player
inventory by using the action addItem('ITEMKEYNAME') or removed by using the
action dropItem('ITEMKEYNAME'). When referencing an item, the actions will
always use ITEMKEYNAME, which must be composed of only alphanumeric characters
and no spaces.

    {
    "Items": {
        "ITEMKEYNAME1":{
                    "name": null,
                    "equipable": false,
                    "statMod": null,
                    "usable": false,
                    "action": null,
                    "effect": null,
                    "reusable": false,
                    "unique": false,
                    "description": false,
                    "category": null,
                    "icon": null
                 },
        "ITEMKEYNAME2":{
                ...
                }
                ...
        }
    }

The file must have a top level statement `Items`, which will start a dictionary
containing the items. Items are referenced by their key names. You can define
how many different items as you like.

Each item then can have one of the following fields defined along. Above are the
default values for all fields. All fields of an item is optional, so you can
only include what is necessary to describe that item.

- `name` : if this field is not provided, the engine will fill this field with
the value of the ITEMKEYNAME instead. Whenever the name of the item is shown to
the player in the game interface, it will be taken from here.

- `equipable` : if this field is provided and has the value true, this item will
have an option to equip it, and a property `equiped=false`. If you select equip,  
the value of `equiped` will be set to `true`. Also, if the item has a `statMod`,
it will be applied. An item should not be `equipable` and `usable` at the same
time.

- `statMod` : provides how the item modify the stats of the Hero who equips it.
If this field is provided, it must contain the dict below:

    - `{"st": INT,  "dx": INT,  "iq": INT }`

    - `st` : how this item modify the Hero `st` attribute.

    - `dx` : how this item modify the Hero `dx` attribute.

    - `iq` : how this item modify the Hero `iq` attribute.

    - You only need to specify the attributes that are modified. For example, `{"st":1}` is a valid value of `statMod`.

- `usable` : if this field is provided and is true, the person playing will have
see an option in the inventory to **use** this item. When the person selects
this option, three things happen: applies the item `effect` if available, then
it's actions are placed in the engine buffer and at last, if the item doesn't
have the property `reusable` set to true, it's dropped.

- `effect` : an effect is a useful way of describing simple `usable` items. If
it is specified, it must accompany the dictionary below:

    - `{"atr":st/iq/dx/null,"basep":INT,"plus":INT,"effect":[EFFECTNAME,...]}`

        - an effect generates a value of points from a dice roll n times and sum the value of `plus`. The n value is `basep` plus the item user's attribute `atr`.

        - the number of poins is then passed to effect, that is a list containing a effect. These can be any of:

            - `hpup` : adds to the item user's hp.

            - more effects are going to be specified as the project evolves.

    - example : `{"plus":10,"effect":["hpup"]}`

- `action` : the effect is useful to generally describing battle relevant items,
but sometimes you need a more complex item. This can usually be accomplished with
action, that can contain a list of actions and parameters that are placed on the
engine buffer when the item is used.

- `reusable` : if this field is specified and is `true`, using the item doesn't
cause it to be dropped.

- `unique` : you can't have more than one of this item, also it can't be purposely
dropped by the player. Unique items are usually meaningful to the storyline of
the game.

- `description` : a string containing the description of the item, think on the
description as the shortest as possible sentence that you could say about the
item by looking at it.

- `category` : the item category is a single word (alphanumeric without spaces)
string. The recommended values are `consumable`, `collectible`, `weapon` and
`armor`. You could specify other values for your particular game implementation,
but you must support these. They are only useful for filtering the inventory
or comparing.

- `icon` : if specified, it is an integer specifying in the `printer.png` which
64x64 pixel image should be used to draw the item in the menu.

## Charaset

A **charaset** is a description of the frames that compose the animations.
When a **chara** is presented to the screen (example: NPCs you interact with),
it will have a drawing in the screen, each chara is associated to a charaset
describing it. At minimum, each chara has two animations: standing, and walking,
each having at least a frame assigned per facing direction. A facing direction
is always one the following: `down`, `right`, `up`, `left`.

    { "Charaset": {
        "tileImage": "charaset.png",
        "CHARASET_NAME": {
            "standing": {
                "down":
                    [[  X,  Y], [  X,  Y], [  X,  Y]...],
                "right":
                    [[  X,  Y]...],
                "up":
                    [[  X,  Y]...],
                "left":
                    [[  X,  Y]...] },
            "walking": {
                "down":
                    [[  X,  Y]...],
                "right":
                    [[  X,  Y]...],
                "up":
                    [[  X,  Y]...],
                "left":
                    [[  X,  Y]...] },
             ...
            },
        ....
        } }

A frame is described by a piece that is 64 pixels in height and 32 pixels in
width of the `tileImage` indicated. This `tileImage` path is relative to the
`img` folder.

The image will be divided in a grid, where each cell has 64 pixels in height
and 32 pixels in width. The first cell at top left is where X and Y are both
zeros. Each cell in horizontal line towards right increments 1 to X, and
each cell in vertical line towards bottom increments 1 to Y. You can have as
many frames as necessary.

You can define other animations with different names, as necessary.

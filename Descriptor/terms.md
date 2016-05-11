Through the development of the engine and the editor, I've choose terms that felt appropriate to the elements they represent - many of them I learned when very young playing in RPG Maker 2000.

## Tile
In this conception, the tile is the minimal element that a map can be split - and the map is built from a tile-map. A tile contain information on it's type, and the type can have meanings - to the engine, the player and the screen.
In the Maker the tile contains the tiles in that location in all layers

## Layers
The game uses 6 layers, which 5 five are real tile map layers. Actually the layers are a virtual process to make it easier to understand how the drawing process works and one could argue it uses several more layers.

## Tile type
The tile type is the number assigned to a cell - in the matrix of numbers that represent the tile map. This number will correspond to an image when in the layers 1,2 and 4, an event in the events layer or an obstacle in the collision layer.
The editor threats tiles in the same position in all layers as a single tile that has five types: one for each layer.

## Tileset
The tileset is a direct dictionary where numbers mean images, this is used to translate the numbers in a tilemap to graphics.

## Palette
A palette contain a textual description of a tileset, along with additional content needed in the tileset translation - like animations and others.

## Chara
A chara is a complete description of a character needed for the engine. For each chara, information on drawing is stored in the charaset.

## Charaset
A charaset is a description of animations and images, that contains at least standing and walking animations for each possible direction the chara can be facing.

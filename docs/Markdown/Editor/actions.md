# Actions

Whenever something happens, what happens, are actions!

Actions are usually not alone, the is usually some list that has actions in a
certain order to be executed.

A list of the available actions is presented below.

## ![](actions/icons/showText.png) showText
Parameter: "text"

**showText** presents a text to the player and blocks, waiting for him to
interact. Currently it supports text wrapping and shows a word per time, and
plays a small noise for each word.

This is a very important part that can be a lot more complex than it seems, like
supporting multiple sounds, characters for pausing, auto skipping text and all,
which can give each conversation bigger depth. Right now, though, I have no
idea how to implement everything in a nice way.


## ![](actions/icons/alert.png) alert
Parameter: "text"

**alert** is a way to show quick texts, that doesn't require the player to
interact.


## ![](actions/icons/teleport.png) teleport
Parameter:"positionx", "positiony", "level"


**teleport** enables moving in a single frame the player from anywhere in the screen to a defined position at a defined level and it's usually meant to be used in doors in a dungeon or town.


## ![](actions/icons/teleportInPlace.png) teleportInPlace
Parameter: "level"

**teleportInPlace** enables moving in a single frame the player from a map to
another map, preserving the player exact position.


## ![](actions/icons/addItem.png) addItem
Parameter: "item"

**addItem** adds an item to the player inventory.


## ![](actions/icons/dropItem.png) dropItem
Parameter: "item"

**dropItem** drops one item from the player inventory.



## ![](actions/icons/changeTile.png) changeTile
Parameter:"tileType","layer","colision","event",["positionx","positiony","level"]/["current"]


**changeTile** can change a tile from a type, to any other type and also change that tile event mark and remove or add colision. It can also target a specific position in a level or just the current tile that contains the event. It's a very powerful action and adds a lot of possibilities.


## ![](actions/icons/changeAllTiles.png) changeAllTiles
Parameter: "tileType", "tileType", "layer", "colision", "event", "level"

**changeAllTiles** changes a single tile that has a type the chosen layer, for
another tile of different type. You can also set those tiles to a different
value of colision or event number.


## ![](actions/icons/changePlayerAnimation.png) changePlayerAnimation
Parameter: "charaset_animation"

**changePlayerAnimation** changes the current player animation. You can set to
default to let animations flow as usual.


## ![](actions/icons/rain.png) rain
Parameter:"start/stop"

**rain** makes rain. You can stop the rain using stop.


## ![](actions/icons/fadeOut.png) fadeOut
Parameter:"effect", "keepEffect"

**fadeOut** fades the screen using a effect and can optionally keep that effect,
usually when you want to do something in between and then play a fadeIn.


## ![](actions/icons/fadeIn.png) fadeIn
Parameter:"effect", "keepEffect"

**fadeIn** is similar to fadeOut, but instead it's meant to bring the screen
back from a fadeOut.


## ![](actions/icons/setVar.png) setVar
Parameter:"variable","value"

**setVar** allow to change a Variable to a specific value. Value can be a number, a string or a special string. Right now the only supported special string is "var:varname", where varname should be changed to the name of a variable which the value you want to pass to the Variable - the first parameter.


## ![](actions/icons/varPlusOne.png) varPlusOne
Parameter:"variable"

**varPlusOne** sums integer 1 on variable. If variable doesn't exist, it creates it!


## ![](actions/icons/waitCycle.png) waitCycle
Parameter:"int"

**waitCycle** blocks the player for a number of specified cycles.


## ![](actions/icons/IF.png) IF
Parameter:"condition"

**IF** condition is a special type of parameter, right now it must be in the format "varOrValue1;oper;varOrValue2", where oper is the operator (right now only "bigger", "smaller" and "equal"). If varOrValue is to be a variable, must be written in the format "var:varname".


If the condition is met, this is, it evaluates to TRUE, then it runs whatever code is next until ELSE or END action are met, and jumps to after the END. If the condition is FALSE  then it ignores any actions until ELSE or END.


## ![](actions/icons/ELSE.png) ELSE
Parameter: ""

**ELSE** is to be used with IF action.


## ![](actions/icons/END.png)  END
Parameter: ""

**END** is to be used with IF action.


## ![](actions/icons/noEffect.png)  noEffect
No parameter

This a placeholder, but it's meant to turn off all effects, like the ones from fadeIn and fadeOut.



[*back*](Editor.md)

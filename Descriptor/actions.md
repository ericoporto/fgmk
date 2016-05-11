Each event (be map event or chara event) can contain actions. Actions are arranged in a list and this list is similar to a receipt with branches - or an algorithm. Actions are the customizable mechanics in which you can script the logics that make things happen and the game progress other than the basic engine.

Here is the list of the actions currently available and the planned one until now.

## showText
Parameter: "text"

showText presents a text to the player. Currently it supports text wrapping and shows a word per time, and plays a small noise for each word. This is a very important part that can be a lot more complex than it seems, like supporting multiple sounds, characters for pausing, auto skipping text and all, which can give each conversation bigger depth. Right now, though, I have no idea how to implement everything in a nice way.

## fadeIn
Parameter:"effect", "keepEffect"

fadeIn fades the screen using a effect and can optionally keep that effect - usually when you want to do something in between and then play a fadeOut.

## fadeOut
Parameter:"effect", "keepEffect"

the same of fadeIn, but instead it's meant to bring the screen back from a fadeOut.

## noEffect
No parameter

This a placeholder, but it's meant to turn off all effects, like the ones from fadeIn and fadeOut.

## teleport
Parameter:"positionx", "positiony", "level"

Teleport enables moving in a single frame the player from anywhere in the screen to a defined position at a defined level and it's usually meant to be used in doors in a dungeon or town.

## changeTile
Parameter:"tileType","layer","colision","event",["positionx","positiony","level"]/["current"]

changeTile can change a tile from a type, to any other type and also change that tile event mark and remove or add colision. It can also target a specific position in a level or just the current tile that contains the event. It's a very powerful action and adds a lot of possibilities.

## setVar
Parameter:"variable","value"

setVar allow to change a Variable to a specific value. Value can be a number, a string or a special string. Right now the only supported special string is "var:varname", where varname should be changed to the name of a variable which the value you want to pass to the Variable - the first parameter.

## varPlusOne
Parameter:"variable"

Sums integer 1 on variable. If variable doesn't exist, it creates it!

## IF
Parameter:"condition"

Condition is a special type of parameter, right now it must be in the format "varOrValue1;oper;varOrValue2", where oper is the operator (right now only "bigger", "smaller" and "equal"). If varOrValue is to be a variable, must be written in the format "var:varname".

If the condition is met, this is, it evaluates to TRUE, then it runs whatever code is next until ELSE or END action are met, and jumps to after the END. If the condition is FALSE  then it ignores any actions until ELSE or END.

## ELSE
Parameter: ""

To be used with IF action.

## END
Parameter: ""

To be used with IF action.


# Planned actions

This is a list of planned actions.

* Get item
* Remove item
* Change chara charaset
* Move chara
* Flash screen
* Shake screen
* While
* Feedback

# Planned properties

This needs to be move to a correct section, but right now there isn't:
* Pushable objects
* Hangable object

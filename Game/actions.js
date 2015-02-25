var actions = {};

lastBlock = function() {
    var value = 0
    var bstk = actions.blockStack.slice(0)
    if(bstk.length>1){
        value = bstk[bstk.length-1];
    } else if(bstk.length==1){
        value = bstk[0];
    }
    return value
}


actions.charAutoDelete = function(param, position, charatodel){
    var params = param.split(';')
    engine.atomStack.push([engine.charAutoDelete,params,charatodel])
}

actions.questionBox = function(param, position){
    var params = param.split(';')
    engine.questionBoxAnswer = engine.questionBoxUndef
    engine.atomStack.push([engine.questionBox,params])
    engine.atomStack.push(["block",null]);
    engine.atomStack.push(["block",null]);
}

actions.stopPicture = function(param, position){
    engine.atomStack.push([engine.stopPicture,''])
}

actions.showPicture = function(param, position){
    var params = param.split(';')
    engine.atomStack.push([engine.showPicture,params])
}

actions.changeState = function(param, position){
    var params = param.split(';');
    engine.atomStack.push([engine.changeState,params])
}

actions.IF = function( param, position ) {
    var params = param.split(';');
    actions.blockCounter++;
    actions.blockStack.push(actions.blockCounter.valueOf());
    engine.atomStack.push([engine.IF,params,lastBlock()] );
}

actions.ELSE = function( param, position ) {
    engine.atomStack.push([engine.ELSE,'',lastBlock()] );
}

actions.END = function( param, position ) {
    engine.atomStack.push([engine.END,'',lastBlock()] );
    var popped = actions.blockStack.pop();
}

actions.preText = function(text) {
    var pretexted = text.slice(0)
    return (text.slice(0)).replace(/(var:)([a-zA-Z0-9]+)/g,
    function(varname){return engine.evalNum(varname)} )
}

actions.showStatus = function(param,position) {
    var params = param.split(';')
    var herotoshow = battle.heroes[params[0]]
    engine.atomStack.push([function(herotosh){battle.herotoshowstatus = herotosh},herotoshow]);
    engine.atomStack.push([engine.waitForKey,true]);
    engine.atomStack.push(["block",null]);
    engine.atomStack.push([function(){battle.herotoshowstatus = false;engine.waitTime(400);},'']);
};

actions.showText = function(param,position) {
    text = actions.preText(param)
    engine.atomStack.push([printer.showText,text]);
    var linesTotal = printer.textLines(text)
    var lineNumber ;
    for (lineNumber = 0 ; lineNumber < linesTotal; lineNumber+=2) {
        engine.atomStack.push([engine.waitForKey,true]);
        engine.atomStack.push(["block",null]);
        engine.atomStack.push([function(){printer.nextLine();engine.waitTime(400);},'']);
    }
};

actions.teleport = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([function(){screen.paused = true;},'']);
    engine.atomStack.push([engine.teleport,params]);
    engine.atomStack.push([function(){screen.paused = false;},'']);
};

actions.changeTile = function(param,position) {
    //param[4] location (current or x,y,level)
    var colisionDict = { keep: -1, noColision: 0 , collidable: 1 }
    var params3Value
    var params = param.split(';')

    var aTileType = params[0]
    var aLayer = params[1]
    var aColision = colisionDict[params[2]];
    if(params[3]=="keep") {
        params3Value = -1;
    } else if(params[3]=="remove") {
        params3Value = 0;
    } else {
        params3Value = parseInt(params[3],10);
    }

    var aEvent = params3Value;
    var aPositionX
    var aPositionY
    var aLevel

    if(params[4]=="current") {
        aPositionY=parseInt(position[0],10)
        aPositionX=position[1]
        aLevel=null
    } else {
        aPositionX=params[4]
        aPositionY=params[5]
        aLevel=params[6]
    }

    engine.atomStack.push([engine.changeTile,[aTileType,
        aLayer, aColision, aEvent, aPositionY, aPositionX,
        aLevel ] ]);
};

actions.fadeIn = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([screen.effects.fadeIn,params]);
    for(var i=0; i < 8; i++) {
        engine.atomStack.push(["block",null]);
    }
};


actions.fadeOut = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([screen.effects.fadeOut,params]);
    for(var i=0; i < 8; i++) {
        engine.atomStack.push(["block",null]);
    }
};

actions.setVar = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([engine.setVar,params]);
};

actions.varPlusOne = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([engine.varPlusOne,params]);
};

actions.testVar = function(param,position) {
    var params = param.split(';')
    engine.atomStack.push([engine.testVar,params]);
};

actions.noEffect = function(param,position) {
    engine.atomStack.push([screen.effects.noEffect,'']);
};


actions.battle = function(param,position) {
    var params = param.split(';')
    actions.fadeOut('tension1;keepEffect')
    dist.setup(screen.canvas,'bgimg1',1)
    actions.changeState('battle')
    engine.atomStack.push([engine.battle,params]);
};

actions.addItem = function(param,position){
    var params = param.split(';')
    engine.atomStack.push([engine.addItem,params]);
}

actions.proceedBattleTurn = function(param,position){
    battle.herodecision = ""
    engine.questionBoxAnswer = engine.questionBoxUndef
    engine.atomStack.push([engine.proceedBattleTurn,[""]])
}

actions.alert = function(param, position){
    var params = param.split(';')

    engine.atomStack.push([engine.alert,params])
}

actions.rain = function(param, position){
    var params = param.split(';')

    if(params[0]=='start'){
        engine.atomStack.push([function(){screen.rains.startRain() },[""]])
    } else {
        engine.atomStack.push([function(){screen.rains.stopRain() },[""]])
    }
}

//Copyright Erico 2015
//This work must not be copied and all assets here are proprietary.
//most r play first
//w is used to attack
//m is used to magic
//target:"hero","weakest","splash","vengeful"
battle = {};
battle.atk = {};
battle.skl = {};
battle.action = {};
battle.effect = {};

battle.setup = function(){

    battle.maxlevel = 99;
    battle.order = new Array();
    battle.heroes = clone(resources.hms.Heroes)

    for (var hero in battle.heroes) {
        battle.initHero(battle.heroes[hero])
    }
}

battle.initHero = function(hero){
    hero["side"] = "hero"
    hero["xp"] = 0
    hero["level"] = 0
    hero["xpnextlevel"] = hero["ExpToLevel"][0]*hero["level"]+hero["ExpToLevel"][1]
    hero["skill"]=[]
    hero["hp"] = 0
    hero["hpmax"] = 0
    battle.uplevel(hero,1,true)
}

battle.initMonster = function(monster){
    monster["side"] = "monster"
    monster["level"] = 0
    monster["skill"]=[]
    monster["hp"] = 0
    monster["hpmax"] = 0
    battle.setMonsterLevel(monster)
    if(!("prob" in monster)) {
        var prob = {}
        var totalprob = 0
        var atks = clone(monster["skill"])
        atks.push("atk")
        for(var i = 0; i < atks.length; i++){
            if(i==atks.length -1){
                prob[atks[i]]=1-totalprob
            } else {
                totalprob+= 1.0/atks.length
                prob[atks[i]]=1.0/atks.length
            }
        }
        monster["prob"] = prob
    }
    monster["xpreward"] = monster["ExpToLevel"][0]*monster["level"]+monster["ExpToLevel"][1]
    monster["dead"]=false
}

battle.uplevel = function(hero, leveltoup, silent){
    var silent = (typeof silent === "undefined") ? false : silent;

    var currlvl = hero["level"]
    hero["w"]  =Math.floor(leveltoup*hero["baseStats"]["w"]/battle.maxlevel)
    hero["r"]  =Math.floor(leveltoup*hero["baseStats"]["r"]/battle.maxlevel)
    hero["m"]  =Math.floor(leveltoup*hero["baseStats"]["m"]/battle.maxlevel)
    hero["hp"] =Math.floor(leveltoup*hero["baseStats"]["hp"]/battle.maxlevel)
    hero["hpmax"] =Math.floor(leveltoup*hero["baseStats"]["hp"]/battle.maxlevel)

    for(var i = currlvl+1; i < leveltoup+1; i++) {
        var lvl = i.toString()
        var text=hero["name"]+" reached level "+lvl+"!"
        hero["level"] = i
        hero["xpnextlevel"] = hero["ExpToLevel"][0]*hero["level"]+hero["ExpToLevel"][1]
        if (lvl in hero["Pathway"]) {
            if ("learn" in hero["Pathway"][lvl]) {
                var tolearn = hero["Pathway"][lvl]["learn"]
                for (var stuff in tolearn){
                    hero[stuff].push(tolearn[stuff])
                    text += "\n"+hero["name"]+" learned "+tolearn[stuff]+"!"
                }
            }
            if ("forget" in hero["Pathway"][lvl]){
                var toforget = hero["Pathway"][lvl]["forget"]
                for (var stuff in toforget){
                    removeA(hero[stuff],toforget[stuff])
                    text += "\n"+hero["name"]+" forgot "+toforget[stuff]+"!"
                }
            }
            if(!silent){
                actions.showText(text)
            }
        }
    }
}

battle.setMonsterLevel = function(mon){
    var mlevel = 0
    for (var i = 0; i < player.party.length; i++) {
        mlevel += battle.hero[i].level
    }

    mlevel = Math.floor(mlevel/player.party.length)
    mlevel += battle.diceroll(1) + player.party.length
    mlevel = Math.max(mlevel-3,1)

    battle.uplevel(mon,mlevel,true)
}

getkey0 = function(tree,key){
    //if key exists return value, otherwise return zero
    if(key in tree)
        return tree[key]
    else
        return 0
}

battle.selectFromProb = function(probdict){
    var random = Math.random();
    var range = 0.0;
    for (atsk in probdict) {
        if(range <= random && random <= range+probdict[atsk])
            return atsk
        range+=probdict[atsk]
    }
}

battle.diceroll = function(n){
    var i = n;
    var result = 0;
    while (i > 0){
        i--
        result+=Math.floor(Math.random()*3+1)
    }
    return result
}



battle.action.atk = function(){
    actions.showText("attack!")
}

battle.action.skill = function(skill){
    actions.showText(skill)
}

battle.start = function(monsterlist){
    battle.holdAtomStack = engine.atomStack
    engine.atomStack=new Array();
    battle.monster = [];
    battle.hero = [];
    battle.waitherodecision = false
    battle.bchToAttack = []
    battle.ended = false
    battle.xpreward = 0;

    if(monsterlist.length>1){
        dist.efnumb[0]=31
    }

    for (var i = 0; i < player.party.length; i++) {
        battle.hero[i] = battle.heroes[player.party[i]]
    }

    for (var i = 0; i < monsterlist.length; i++) {
        battle.monster[i] = clone(resources.hms.Monsters[monsterlist[i]])
        battle.initMonster(battle.monster[i])
    }


    battle.skills = resources.hms.Skills

    battle.setOrderStack();
    actions.fadeIn('blackFadeIn;doNotKeep')

}

battle.resolveOrder = function() {
    if(battle.ended) {
        return
    }

    if(!battle.waitherodecision) {
        if(battle.order.length > 0){
            battle.bchToAttack = battle.order.shift();
            if(battle.bchToAttack[1]=="hero") {
                console.log("hero attack")
                if(battle.resolveIfSideDead()) {
                    return
                }
                battle.herodecision = "action"
                actions.questionBox("attack;skill")
                battle.waitherodecision = true
                if(battle.resolveIfSideDead()) {
                    return
                }
            } else {
                console.log("monster attack")
                if(battle.resolveIfSideDead()) {
                    return
                }
                if(!(battle.bchToAttack[0].dead)){
                    battle.mAttack(battle.bchToAttack[0])
                }
                if(battle.resolveIfSideDead()) {
                    return
                }
            }
        } else {
            if(battle.isPartyAlive()) {
                battle.setOrderStack()
            }

        }
    } else {
        battle.hAttack(battle.bchToAttack[0])
    }
}

battle.resolveIfSideDead = function(){
    if(!(battle.isPartyAlive())){
        while(battle.order.length > 0) {
            battle.order.pop();
        }
        battle.ended = true
        actions.showText("You died!")
        battle.end("died")
        return true
    }
    if(!(battle.isMonstersAlive())){
        while(battle.order.length > 0) {
            battle.order.pop();
        }
        battle.ended = true
        actions.showText("You win!")
        battle.end("win")
        return true
    }
    return false
}

battle.setOrderStack = function(){
    while(battle.order.length > 0) {
        battle.order.pop();
    }
    for (var i = 0; i < player.party.length; i++) {
        battle.order.push([battle.hero[i],"hero"]);
    }
    for (var i = 0; i < battle.monster.length; i++) {
        battle.order.push([battle.monster[i],"monster"]);
    }
    battle.order.sort( function(a,b) {
        if (a[0]["r"] > b[0]["r"])
            return -1;
        if (a[0]["r"] < b[0]["r"])
            return 1;
        return 0;
    } );
}

battle.hAct = {}
battle.hAct.askTarget = function(){
    engine.questionBoxAnswer = engine.questionBoxUndef
    battle.hAct.targetting = true
    battle.herodecision = "target"
    var selmon = []
    for(var i=0; i<battle.monster.length;i++){
        if(!(battle.monster[i].dead)){
            selmon.push(battle.monster[i])
        }
    }

    if(selmon.length == 1){
        selmon[0].selected = false
        battle.hAct.targetting = false
        battle.hAct.__target = [selmon[0]]
        engine.questionBoxAnswer = 0
        HID.inputs["accept"].active = false
        return
    }

   //the selectable monsters
    for(var i=0; i<selmon.length;i++){
        selmon[i].selected = false
        selmon[i].flash = 0

        if ( i == 0) {
            selmon[i].previous = selmon[0]
            selmon[i].next = selmon[i+1]
        } else if (i == selmon.length-1) {
            selmon[i].previous = selmon[i-1]
            selmon[i].next = selmon[i]
        } else {
            selmon[i].previous = selmon[i-1]
            selmon[i].next = selmon[i+1]
        }

    }
    selmon[0].selected = true
    battle.hAct.selectedMonster = selmon[0]
}

battle.hAct.changeSelection = function(next){
    battle.hAct.selectedMonster.selected = false
    battle.hAct.selectedMonster = battle.hAct.selectedMonster[next]
    battle.hAct.selectedMonster.selected = true
}

battle.hAct.targetUpdate= function(){
    if(typeof this.keyPressed === "undefined" ){
        this.keyPressed = 0
    }

    if(this.keyPressed==0) {
        if(HID.inputs["up"].active){
            battle.hAct.changeSelection('previous')
            HID.inputs["up"].active = false
            this.keyPressed=32
        }else if(HID.inputs["left"].active){
            battle.hAct.changeSelection('previous')
            HID.inputs["left"].active = false
            this.keyPressed=32
        }else if(HID.inputs["right"].active){
            battle.hAct.changeSelection('next')
            HID.inputs["right"].active = false
            this.keyPressed=32
        }else if(HID.inputs["down"].active){
            battle.hAct.changeSelection('next')
            HID.inputs["down"].active = false
            this.keyPressed=32
        }else if(HID.inputs["accept"].active){
            this.selectedMonster.selected = false
            battle.hAct.targetting = false
            battle.hAct.__target = [battle.hAct.selectedMonster]
            engine.questionBoxAnswer = 0
            HID.inputs["accept"].active = false
            this.keyPressed=32
        }else if(HID.inputs["cancel"].active){

        }
    } else {
        this.keyPressed-=4
    }
}

battle.hAttack = function(hero){
    //select action
    //if attack or skill select target
    //resolve
    if(engine.questionBoxAnswer != engine.questionBoxUndef && battle.herodecision == "action"){
        if(engine.questionBoxAnswer == 0 ) {
            battle.hAct.__damage = battle.atk.pts(hero)
            battle.hAct.__actionType = ["hpdown"]
            battle.hAct.__skill = "atk"
            if(battle.monster.length <= 1){
                battle.hAct.__target = [battle.monster[0]]
                var __proceed = true
            } else {
                battle.hAct.askTarget()
            }
        } else if(engine.questionBoxAnswer == 1){
            battle.herodecision = "skill"
            var options = hero["skill"].join(";")
            options="back;"+options
            actions.questionBox(options)
        }
    }
    if(engine.questionBoxAnswer != engine.questionBoxUndef && battle.herodecision == "skill"){
        if(engine.questionBoxAnswer==0) {
            battle.herodecision = "action"
            actions.questionBox("attack;skill")
        } else {
            actions.showText(engine.questionBoxAnswerStr)
            battle.hAct.__damage = battle.skl.pts(hero,engine.questionBoxAnswerStr)
            battle.hAct.__actionType = battle.skills[engine.questionBoxAnswerStr].effect
            battle.hAct.__target = [battle.monster[0]]
            battle.hAct.__skill = engine.questionBoxAnswerStr
            var __proceed = true
        }

    }
    if(engine.questionBoxAnswer != engine.questionBoxUndef && battle.herodecision == "target"){
        var __proceed = true
    }
    if(typeof __proceed !== "undefined" ){
        if(__proceed != false){
            console.log("attacked")
            battle.resolveAtk(hero, battle.hAct.__target, battle.hAct.__damage,
                battle.hAct.__actionType, battle.hAct.__skill)
            actions.proceedBattleTurn()
        }
    }
}

battle.mAttack = function(mn){
    var mon = mn
    var attack = battle.selectFromProb(mon["prob"])
    var damage = 0
    var actionType = []
    var target = [battle.mTarget(mon)]

    if(attack=="atk") {
        damage = battle.atk.pts(mon)
        actionType = ["hpdown"]
    } else {
        damage = battle.skl.pts(mon,attack)
        actionType = battle.skills[attack].effect
        if(battle.skills[attack].affect=="all")
            target = battle.hero
    }

    if(damage>0){
        screen.flashMonster(mon,'#eeeeee')
    } else {
        screen.shakeMonster(mon)
    }

    battle.resolveAtk(mon, target, damage, actionType, attack)
}

battle.resolveAtk = function(bchSrc, bchVct, dmg, act, skill){
    //for each victim, do the effect applying damage
    for (var j = 0; j < bchVct.length; j++) {
        for (var i = 0; i < act.length; i++) {
            battle.effect[act[i]](bchSrc,bchVct[j],dmg, skill)
        }
    }
}

battle.effect.hpdown = function(bchsrc,bch,dmg, skill){
    bch.hp = Math.max(bch["hp"]-dmg, 0)
    if(skill == "atk") {
        actions.showText(bchsrc.name+" attacked "+ bch.name+" and dealt "+dmg+" damage!")
    } else {
        actions.showText(bchsrc.name+" used "+skill+" on "+ bch.name+" and dealt "+dmg+" damage!")
    }
    if(bch.side == "monster"){
        screen.flashMonster(bch, '#bf0010')
    }
}

battle.effect.hpup = function(bchsrc, bch,dmg){
    bch.hp = Math.min(bch["hp"]+dmg, bch["hpmax"])
}

battle.mTarget = function(monster){
    var dead = true
    if(monster.target=="splash"){

    } else if(monster.target=="hero"){
        var options = battle.hero.length

        for (var i = 0; i < options; i++) {
            if(battle.hero[i].Leader && battle.isAlive(battle.hero[i])) {
                return battle.hero[i]
            }
        }


    } else if(monster.target=="weakest") {
        var minhp = 999999999
        var index = 0
        for (var i = 0; i < options; i++) {
            if(battle.hero[i].hp < minhp && battle.hero[i].hp > 0) {
                minhp = battle.hero[i]["hp"]
                index = i
            }
        }
        return battle.hero[index]
    }

    var target = 0
    var options = battle.hero.length
    var targetProb = {}
    for (var i = 0; i < options; i++) {
        targetProb[i] = 1/options
    }


    var tries = 0

    while(dead){
        tries++
        target = battle.selectFromProb(targetProb)
        dead = !battle.isAlive(battle.hero[target])
        if(tries > 20) {
            break
        }
    }

    return battle.hero[target]
}

battle.end = function(battleresult) {
    battle.lastresult = battleresult
    for (var i = 0; i < battle.hero.length; i++){
        if(battle.isAlive(battle.hero[i])){
            var thishero = battle.hero[i]
            thishero.xp+=Math.floor(battle.xpreward/battle.hero.length)
            thishero.xpnextlevel = thishero.ExpToLevel[0]*thishero.level+thishero.ExpToLevel[1]
            while(thishero.xp > thishero.xpnextlevel){
                var newlevel = thishero.level + 1
                battle.uplevel(thishero,newlevel)
                thishero.xpnextlevel = thishero.ExpToLevel[0]*thishero.level+thishero.ExpToLevel[1]
            }
        }
    }
    actions.changeState("map")
    engine.atomStack.push([function(){engine.atomStack = battle.holdAtomStack },''])
}

battle.isPartyAlive = function() {
    var test = 0
    for (var i = 0; i < battle.hero.length; i++){
        test += battle.isAlive(battle.hero[i])
    }
    return (test > 0)
}

battle.monsterDies = function(monster){
    battle.xpreward += monster.xpreward
}

battle.isMonstersAlive = function() {
    var test = 0
    for (var i = 0; i < battle.monster.length; i++){
        test += battle.isAlive(battle.monster[i])
        if(!(battle.isAlive(battle.monster[i]))){
            if(!(battle.monster[i].dead)){
                battle.monster[i].dead = true
                battle.monsterDies(battle.monster[i])
            }
        }
    }
    return (test > 0)
}

battle.isAlive = function(bch){
    return (bch["hp"] > 0)
}

battle.atk.pts = function(bch){
    return battle.diceroll(bch["w"])
}

battle.skl.pts = function(bch,skill){
    var baseplus = getkey0(battle.skills[skill],"basep")
    var plus = getkey0(battle.skills[skill],"plus")
    var attribut = 0
    if("atr" in battle.skills[skill])
        attribut = bch[battle.skills[skill]["atr"]]

    return Math.max(battle.diceroll(baseplus+attribut)+plus,0)
}

battle.mApplyState = function(mon,st) {
    for(var k in mon.state[st]){
        mon[k] = mon.state[st][k]
    }
}

battle.update = function(){
    battle.resolveOrder();
    if(battle.hAct.targetting){
        battle.hAct.targetUpdate();
    }

}

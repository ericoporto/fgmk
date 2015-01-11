//most r play first
//w is used to attack
//m is used to magic
//target:"hero","weakest","splash","vengeful"
battle = {};
battle.atk = {};
battle.skl = {};
battle.action = {};
battle.effect = {};
battle.maxlevel = 99;
battle.initHero = function(hero){
    hero["xp"] = 0
    hero["level"] = 0
    hero["xpnextlevel"] = hero["ExpToLevel"][0]*hero["level"]+hero["ExpToLevel"][1]
    hero["skill"]=[]
    hero["hp"] = 0
    hero["maxhp"] = 0
    battle.uplevel(hero,1,true)
}

battle.initMonster = function(monster){
    monster["level"] = 0
    monster["skill"]=[]
    monster["hp"] = 0
    monster["maxhp"] = 0
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
}

battle.uplevel = function(hero, leveltoup, silent){
    var silent = (typeof silent === "undefined") ? false : silent;

    var currlvl = hero["level"]
    hero["w"]  =Math.floor(leveltoup*hero["baseStats"]["w"]/battle.maxlevel)
    hero["r"]  =Math.floor(leveltoup*hero["baseStats"]["r"]/battle.maxlevel)
    hero["m"]  =Math.floor(leveltoup*hero["baseStats"]["m"]/battle.maxlevel)
    hero["hp"] =Math.floor(leveltoup*hero["baseStats"]["hp"]/battle.maxlevel)
    hero["maxhp"] =Math.floor(leveltoup*hero["baseStats"]["hp"]/battle.maxlevel)

    for(var i = currlvl+1; i < leveltoup+1; i++) {
        var lvl = i.toString()
        var text=hero["name"]+" reached level "+lvl+"!"
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

battle.setup = function(){

    battle.heroes = clone(resources.hms.Heroes)

    battle.battlemenu = new menu({
        attack: {
            action: [battle.action.atk],
            index: 0
        },
        skill: {
            action: [function(){ actions.showText("skill!")}],
            index: 0
        },
        item: {
            action: [function(){ actions.showText("item!")}],
            index: 0
        }
    },undefined,true);

}

battle.action.atk = function(){
    actions.showText("attack!")
}

battle.action.skill = function(skill){
    actions.showText(skill)
}

battle.start = function(monsterlist){
    battle.monster = [];
    battle.hero = [];

    for (var i = 0; i < player.party.length; i++) {
        battle.hero[i] = battle.heroes[player.party[i]]
    }

    for (var i = 0; i < monsterlist.length; i++) {
        battle.monster[i] = clone(resources.hms.Monsters[monsterlist[i]])
        battle.initMonster(battle.monster[i])
    }



    battle.skills = resources.hms.Skills

    actions.questionBox("test1;test2;test3")
}

battle.hAttack = function(){
    //select action
    //if attack or skill select target
    //resolve
}

battle.mAttack = function(mn){
    var mon = battle.monster[mn]
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

    battle.resolveAtk(mon, target, damage, actionType)
}

battle.resolveAtk = function(bchSrc, bchVct, dmg, act){
    //for each victim, do the effect applying damage
    for (var j = 0; j < bchVct.length; j++) {
        for (var i = 0; i < act.length; i++) {
            battle.effect[act[i]](bchVct[j],dmg)
        }
    }
}

battle.effect.hpdown = function(bch,dmg){
    bch.hp = Math.max(bch.hp-dmg, 0)
}

battle.effect.hpup = function(bch,dmg){
    bch.hp = Math.min(bch.hp+dmg, bch.hpmax)
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
                minhp = battle.hero[i].hp
                index = i
            }
        }
        return battle.hero[index]
    }

    var target = 0
    var options = battle.hero.length
    var targetProb = {}
    for (var i = 0; i < options; i++) {
        targetProb[i] = i/options
    }

    while(dead){
        target = battle.selectFromProb(targetProb)
        dead = !battle.isAlive(battle.hero[target])
    }
    return battle.hero[target]
}

battle.isAlive = function(bch){
    return (bch.hp > 0)
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
    
}

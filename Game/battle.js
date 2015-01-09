//most r play first
//w is used to attack
//m is used to magic
//target:"hero","weakest","splash","vengeful"
battle = {};
battle.atk = {};
battle.skl = {};
battle.action = {};

battle.initHero = function(hero){
    hero["xp"] = 0
    hero["level"] = -1
    hero["xpnextlevel"] = hero["ExpToLevel"][0]*hero["level"]+hero["ExpToLevel"][1]
    hero["skill"]=[]
    hero["w"] = 0
    hero["r"] = 0
    hero["m"] = 0
    hero["hp"] = 0
    battle.uplevel(hero,0)

}

battle.uplevel = function(hero, leveltoup){
    var currlvl = hero["level"]
    for(var i = currlvl+1; i < leveltoup+1; i++) {
        var lvl = i.toString()
        console.log(lvl)
        hero["w"]  +=hero["Pathway"][lvl]["w"]
        hero["r"]  +=hero["Pathway"][lvl]["r"]
        hero["m"]  +=hero["Pathway"][lvl]["m"]
        hero["hp"] +=hero["Pathway"][lvl]["hp"]
        if ("learn" in hero["Pathway"][lvl]) {
            var tolearn = hero["Pathway"][lvl]["learn"]
            for (var stuff in tolearn){
                hero[stuff].push(tolearn[stuff])
            }
        }
        if ("forget" in hero["Pathway"][lvl]){
            var toforget = hero["Pathway"][lvl]["forget"]
            for (var stuff in toforget){
                removeA(hero[stuff],toforget[stuff])
            }
        }
    }
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

    for (var i = 0; i < monsterlist.length; i++) {
        battle.monster[i] = clone(resources.hms.Monsters[monsterlist[i]])
    }

    for (var i = 0; i < player.party.length; i++) {
        battle.hero[i] = clone(resources.hms.Heroes[player.party[i]])
    }

    battle.skills = resources.hms.Skills

    battle.battlemenu.activate()
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
    if(attack=="atk")
        damage = battle.atk.pts(mon)
    else
        damage = battle.skl.pts(mon,attack)
    console.log(attack)
    console.log(damage)
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

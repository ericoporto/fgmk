//most r play first
//w is used to attack
//m is used to magic
//target:"Hero","weakest","splash","vengeful"
battle = {}
battle.atk = {}

getkey0 = function(tree,key){
    //if key exists return value, otherwise return zero
    if(key in tree)
        return tree[key]
    else
        return 0
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

var descriptors = "descriptors/"
var charaset = "charaset/"
var levelsFolder = "levels/"
var charasetsFolder = "charaset/"
var charasFolder = "charas/"
var resources = {
    tileset: null,
    playerChara: null,
    printerset: null,
    playerCharaset: null,
    faceset: null,
    feedback: {},
    items: {},
    levels: {},
    charasets: {},
    charas: {},
    hms: {}
};

resources.harvest = function(){
    var filecount = 0;
    document.getElementsByTagName('canvas')[0].getContext('2d').fillStyle = '#FFFFFF';

    var getresource = function(getthis) {
        var toreturn = jsonGet(getthis)
        if(!(typeof toreturn.resources === "undefined")){
            if(!(typeof toreturn.resources.audio === "undefined")){

            }
        }
        filecount+=1
        if(!(typeof toreturn.Level === "undefined")){
            document.getElementsByTagName('canvas')[0].getContext('2d').fillText(".", filecount, filecount)
        }
        return toreturn
    }

    this.tileset = document.getElementById("tile");
    this.faceset = document.getElementById("faceset");
    this.charasetimg = document.getElementById("charasetimg");
    this.printerset = document.getElementById("printerimg");
    this.monsterimg = document.getElementById("monsterbattleimg");
    this.pictures = {}
    this.pictures.title = document.getElementById("titleimg");
    this.pictures.keys0 = document.getElementById("keys0");
    this.pictures.keys1 = document.getElementById("keys1");
    this.pictures.keys2 = document.getElementById("keys2");
    this.pictures.controllers = document.getElementById("controllers");

    this.feedback = getresource(descriptors+"feedback.json")['Feedback'];

    LevelsList = init['LevelsList']
    for (var level in LevelsList) {
        var levelItem = LevelsList[level]
        console.log(descriptors+levelsFolder+levelItem)
        resources['levels'][level] = getresource(descriptors+levelsFolder+levelItem);
    }
    CharasetFileList = init['CharasetFileList']
    for (var charasetfilep in CharasetFileList) {
        var charasetfile = CharasetFileList[charasetfilep]
        console.log(descriptors+charasetsFolder+charasetfile)
        resources['charasets'] = getresource(descriptors+charasetsFolder+charasetfile)['Charaset'];
    }
    //CharasFileList = init['CharasFileList']
    //for (var charasfilep in CharasFileList) {
    //    var charasfile = CharasFileList[charasfilep]
    //    console.log(descriptors+charasFolder+charasfile)
    //    resources['charas'] = jsonGet(descriptors+charasFolder+charasfile)['Charas'];
    //}

    resources['charas'] = getresource(descriptors+"charas.json")['Charas'];
    this.playerCharaset = resources['charasets'][init['Player']['charaSet']];
    this.hms = getresource(descriptors+init["HMSFile"])
    this.items = getresource(descriptors+init["itemsFile"])['Items']
}

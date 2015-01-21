var bootstrap = {};
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
    levels: {},
    charasets: {},
    charas: {},
	hms: {}
};

window.forceMobile=false

var query = window.location.search.substring(1).split("&");
for (var i = 0, max = query.length; i < max; i++)
{
    if (query[i] === "") // check for trailing & with no param
        continue;

    var param = query[i].split("=");
    if(param[0]=="forceMobile" && (param[1]=="true" ||param[1]=="True" || param[1]=="1"))
        window.forceMobile=true

}


resources.harvest = function(){
	this.tileset = document.getElementById("tile");
    this.charasetimg = document.getElementById("charasetimg");
    this.printerset = document.getElementById("printerimg");
	this.monsterimg = document.getElementById("monsterbattleimg");
	this.pictures = {}
	this.pictures.title = document.getElementById("titleimg");
	this.pictures.keys0 = document.getElementById("keys0");
	this.pictures.keys1 = document.getElementById("keys1");
	this.pictures.keys2 = document.getElementById("keys2");

    LevelsList = init['LevelsList']
    for (var level in LevelsList) {
        var levelItem = LevelsList[level]
        console.log(descriptors+levelsFolder+levelItem)
        resources['levels'][level] = jsonLevelGet(descriptors+levelsFolder+levelItem);
    }
    CharasetFileList = init['CharasetFileList']
    for (var charasetfilep in CharasetFileList) {
        var charasetfile = CharasetFileList[charasetfilep]
        console.log(descriptors+charasetsFolder+charasetfile)
        resources['charasets'] = jsonLevelGet(descriptors+charasetsFolder+charasetfile)['Charaset'];
    }
    //CharasFileList = init['CharasFileList']
    //for (var charasfilep in CharasFileList) {
    //    var charasfile = CharasFileList[charasfilep]
    //    console.log(descriptors+charasFolder+charasfile)
    //    resources['charas'] = jsonLevelGet(descriptors+charasFolder+charasfile)['Charas'];
    //}

    resources['charas'] = jsonLevelGet(descriptors+"charas.json")['Charas'];
    this.playerCharaset = resources['charasets'][init['Player']['charaSet']];
	this.hms = jsonLevelGet(descriptors+init["HMSFile"])
}

window.addEventListener('unload', function (e) { e.preventDefault(); jsonLevelGet("http://127.0.0.1:8081/exit.json");  }, false);


var init = jsonLevelGet(descriptors+'init.json');



bootstrap.onLoadDOM = function(){
	try{
		var child = document.getElementById("loading");
		child.parentNode.removeChild(child);
		document.ontouchmove = function(e){ e.preventDefault();}
		document.getElementsByTagName('canvas')[0].getContext('2d').fillText("LOADING...", 64, 64)
		resources.harvest();
        screen.init();
        player.setup();
        camera.setupCanvas(screen.canvas);
		engine.setup();
        screen.setEngine(engine);
		HID.setup(screen)
        engine.currentLevel = resources['levels'][init['World']['initLevel']];
		screen.printBox.setup(resources.printerset);
		feedbackEng.setup();
		title.setup();
		battle.setup();
		menus.setAllDrawables();
		engine.loop();
		screen.loop();
        debug.FPS.loop();
        chars = new charalist();
        chars.push(player)
	}catch (err){
		alert("Error on bootstrap! "+err);
	}
}

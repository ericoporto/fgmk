var bootstrap = {};

window.forceMobile=false

var query = window.location.search.substring(1).split("&");
for (var i = 0, max = query.length; i < max; i++)
{
    if (query[i] === "") // check for trailing & with no param
        continue;

    var param = query[i].split("=");
    if(param[0]=="forceMobile" && (param[1]=="true" ||param[1]=="True" || param[1]=="1"))
        window.forceMobile=true

	if(param[0]=="debug" && (param[1]=="true" ||param[1]=="True" || param[1]=="1"))
		window.addEventListener('unload', function (e) { e.preventDefault(); jsonGet("http://127.0.0.1:8081/exit.json");  }, false);

}

var init = jsonGet(descriptors+'init.json');

bootstrap.onLoadDOM = function(){
	try{
		var child = document.getElementById("loading");
		child.parentNode.removeChild(child);
		document.ontouchmove = function(e){ e.preventDefault();}
		document.getElementsByTagName('canvas')[0].getContext('2d').fillStyle = '#FFFFFF';
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
		screen.requestAnimationFrame.call(window,function(){screen.loop()})
        debug.FPS.loop();
        chars = new charalist();
        chars.push(player)
	}catch (err){
		alert("Error on bootstrap! "+err);
	}
}

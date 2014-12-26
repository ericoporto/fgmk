

window.addEventListener('resize', screen.resize, false);
window.addEventListener('orientationchange', screen.resize, false);

var camera = {};
//camera.width = 16;
//camera.height = 10;
camera.x = 0;
camera.y = 0;
camera.finex = 0;
camera.finey = 0;

camera.setupMap = function(_worldLevel, _engine){
	this.maxWorldWidth = _worldLevel["Level"]["layer1"][0].length;
	this.maxWorldHeight = _worldLevel["Level"]["layer1"].length;
}

camera.setupCanvas = function(_canvas){
    this.width = Math.floor(screen.GWIDTH/32)+1
    this.height = Math.floor(screen.GHEIGHT/32)+1
    this.halfWidth = Math.floor(this.width/2);
    this.halfHeight = Math.floor(this.height/2);
}

camera.panToChara = function(chara){

    charatilex = Math.floor(chara.mapx/32);
    charatiley = Math.floor(chara.mapy/32)+1;

    if(charatilex > this.halfWidth && charatilex < this.maxWorldWidth - this.halfWidth ) {
            this.x = charatilex;
            this.finex = chara.mapx%32;
    } else {
        if(charatilex == this.halfWidth) {
            this.x = this.halfWidth;
            this.finex = chara.mapx%32;
        } else if (charatilex < this.halfWidth) {
            this.x = this.halfWidth;
        } else if (charatilex == this.maxWorldWidth - this.halfWidth) {
            this.x = this.maxWorldWidth - this.halfWidth;
            this.finex = chara.mapx%32;
        } else  {
            this.x = this.maxWorldWidth - this.halfWidth ;
        }
    }

    if(charatiley > this.halfHeight && charatiley < this.maxWorldHeight - this.halfHeight ) {
            this.y = charatiley;
            this.finey = chara.mapy%32;
    } else {
        if(charatiley == this.halfHeight) {
            this.y = this.halfHeight;
            this.finey = chara.mapy%32;
        } else if (charatiley < this.halfHeight) {
            this.y = this.halfHeight;
        } else if (charatiley == this.maxWorldHeight - this.halfHeight) {
            this.y = this.maxWorldHeight - this.halfHeight;
            this.finey = chara.mapy%32;
        } else  {
            this.y = this.maxWorldHeight - this.halfHeight;
        }
    }

    this.x -= this.halfWidth
    this.y -= this.halfHeight

}

camera.drawMapLayer = function(_worldLevel, _zIndex){

    var targetFrame = Math.floor(screen.frameCount/4)%4;

	var vx = 0, vy =0,
		currentTile, tileNumber;

    var screenx = 0, screeny =0;

    this.panToChara(player)

    initX = Math.max(0,this.x)
    initY = Math.max(0,this.y)
    EndX = Math.min(this.maxWorldWidth,this.x+this.width)
    EndY = Math.min(this.maxWorldHeight,this.y+this.height)


	for(vx = initX, screenx =0; vx < EndX; vx++, screenx++){
		for(vy = initY, screeny =0; vy < EndY; vy++, screeny++){
            tileNumber = _worldLevel.Level[_zIndex][vy][vx]
			currentTile = _worldLevel.Level.tiles[ tileNumber];
            if(_worldLevel.Level.tilesAnimated[tileNumber.toString()]){
                currentTile = _worldLevel.Level.tilesAnimated[tileNumber.toString()][targetFrame]
            }


			if(!currentTile) continue;
			screen.drawTile(resources.tileset, currentTile, [32*screenx-this.finex, 32*screeny-this.finey]);
		}
	}

}

camera.drawChar = function(chara){



	if(chara.steps) charaAnimation = chara['charaset']["walking"][chara.facing]
    else charaAnimation =  chara['charaset']["standing"][chara.facing]

    var targetFrame = Math.floor(screen.frameCount/4)%charaAnimation.length;

    var screenx = 0, screeny =0;

    screenx = chara.mapx-(this.x*32+this.finex)
    screeny = chara.mapy-(this.y*32+this.finey)

    screen.drawChara(resources.playerChara, charaAnimation, targetFrame, [screenx, screeny])

}

printBox = {};
printBox.show = function() {
    screen.printBox.targetFrame = 0
    screen.printBox.anim = 'fadeIn'
}

printBox.isShown = function() {
    if (screen.printBox.anim == 'box') {
        return true
    }
    else {
        return false
    }
}

printBox.close = function() {
        screen.printBox.targetFrame = screen.printBox.frameMax
        screen.printBox.anim = 'fadeOut'
};


var screen = {};
screen.paused = false;
screen.WIDTH = 416;
screen.HEIGHT = 704;
screen.GWIDTH = 416;
screen.GHEIGHT = 416;
screen.GSTARTX= 0;
screen.GSTARTY = 0;
screen.RATIO = null;
screen.currentWidth = null;
screen.currentHeight = null;
screen.canvas = null;
screen.ctx = null;
screen.frameCount = 0;
screen.timer = null;
screen.engine = null;
screen.mobile =false;

screen.setEngine = function(engine) {
	this.engine = engine;
}

screen.drawChara = function(charaset, animation, frameNumber, position) {
	screen.ctx.drawImage(charaset,
		32*animation[frameNumber][0], 64*animation[frameNumber][1],
		32, 64,
		this.GSTARTX+position[0], this.GSTARTY+position[1],
		32, 64);
}

screen.drawTile = function(tileset, tile, position) {
    screen.ctx.drawImage(tileset,
				32*tile[0], 32*tile[1], 32, 32,
				this.GSTARTX+position[0], this.GSTARTY+position[1], 32, 32);
}

screen.init = function() {

    this.RATIO = this.WIDTH / this.HEIGHT;
    this.mobile =window.mobilecheck();
    this.currentWidth = this.WIDTH;
    this.currentHeight = this.HEIGHT;
    this.canvas = document.getElementsByTagName('canvas')[0];
    this.canvas.width = this.WIDTH;
    this.canvas.height = this.HEIGHT;
    this.ctx = this.canvas.getContext('2d');
    this.ctx.font = '32px INFO56';
    this.resize();

    this.ua = navigator.userAgent.toLowerCase();
    this.android = this.ua.indexOf('android') > -1 ? true : false;
    this.ios = ( this.ua.indexOf('iphone') > -1 || this.ua.indexOf('ipad') > -1  ) ? true : false;
    window.addEventListener('load', screen.init, false);

    this.ctx.mozImageSmoothingEnabled = false;
    this.ctx.webkitImageSmoothingEnabled = false;
    this.ctx.imageSmoothingEnabled = false;
}

screen.resize = function() {
    this.ctx.mozImageSmoothingEnabled = false;
    this.ctx.webkitImageSmoothingEnabled = false;
    this.ctx.imageSmoothingEnabled = false;

    if (screen.mobile) {
        this.currentHeight = window.innerHeight;
        this.currentWidth = this.currentHeight * this.RATIO;
    } else {
        this.GHEIGHT=288;
        this.currentHeight = window.innerHeight * this.HEIGHT/this.GHEIGHT
        this.currentWidth = this.currentHeight * this.RATIO;
    }


    if (this.android || this.ios) {
        document.body.style.height = (window.innerHeight + 50) + 'px';
    }

    this.canvas.style.width = this.currentWidth + 'px';
    this.canvas.style.height = this.currentHeight + 'px';

    window.setTimeout(function() {
            window.scrollTo(0,1);
    }, 1);
}

screen.drawButton = function(pHIDItem){
	if(pHIDItem.active)
	    this.ctx.fillStyle = '#ff9900';
    else
	    this.ctx.fillStyle = pHIDItem.color;
	this.ctx.fillRect(pHIDItem.mapX, pHIDItem.mapY+this.GHEIGHT, 96, 96);

    this.ctx.fillStyle = '#FFFFFF';
    this.ctx.fillText(pHIDItem.letter,pHIDItem.mapX+32, pHIDItem.mapY+this.GHEIGHT+64);
}

screen.drawHID = function(){

	this.ctx.fillStyle = '#0000ff';
	this.ctx.fillRect(0, this.GHEIGHT, this.GWIDTH, this.HEIGHT - this.GHEIGHT);

	var HIDItem;
	for(var tag in HID.inputs){
		HIDItem = HID.inputs[tag];
		screen.drawButton(HIDItem)
	}


}

screen.clearAll = function(){
	this.ctx.fillStyle = '#d0e7f9';
	this.ctx.fillRect(this.GSTARTX, this.GSTARTY, this.GWIDTH, this.GHEIGHT);
}


screen.printBox = {

    setup: function(imgPrintSet){
    this.Width = screen.GWIDTH;
    this.Height = 96;
    this.X = 0;
    this.Y = screen.GHEIGHT - this.Height;
    this.imgPrintSet = imgPrintSet;
    this.aSizex = [32, 64, 128, this.Width,  this.Width ];
    this.aSizey = [32, 32,48, 48, this.Height ];
    this.anim = 'none';
    this.frameMax = this.aSizex.length - 1;
    this.targetFrame = this.frameMax;
    },

    printSet:{
        background: {
            x: 0,
            y: 0,
            sizex: 64,
            sizey: 64
        },
        topLeftBox: {
            x: 64,
            y: 0,
            sizex: 16,
            sizey: 16
        },
        topRightBox: {
            x: 112,
            y: 0,
            sizex: 16,
            sizey: 16
        },
        bottomLeftBox: {
            x: 64,
            y: 48,
            sizex: 16,
            sizey: 16
        },
        bottomRightBox: {
            x: 112,
            y: 48,
            sizex: 16,
            sizey: 16
        },
        LeftBox: {
            x: 64,
            y: 16,
            sizex: 16,
            sizey: 32
        },
        RightBox: {
            x: 112,
            y: 16,
            sizex: 16,
            sizey: 32
        },
        TopBox: {
            x: 80,
            y: 0,
            sizex: 32,
            sizey: 16
        },
        BottomBox: {
            x: 80,
            y: 48,
            sizex: 32,
            sizey: 16
        },
        icon0: {
            x: 0,
            y: 96,
            sizex: 64,
            sizey: 64
        },
        icon1: {
            x: 64,
            y: 96,
            sizex: 64,
            sizey: 64
        }
    },


    drawElement: function(element,x,y,sizex,sizey,imgPrintSet, select){
        select = (typeof select === "undefined") ? 0 : select;
        screen.ctx.drawImage(imgPrintSet,
				    element['x']+select*64, element['y'],
                    element['sizex'], element['sizey'],
				    screen.GSTARTX+x, screen.GSTARTY+y, sizex, sizey);
    },

    drawBoxAnimation: function(){
        if(this.anim == 'none') {
            return
        } else if(this.anim == 'box') {
            this.targetFrame = this.frameMax
        } else if(this.anim == 'fadeIn') {
            if ( this.targetFrame < this.frameMax)
                this.targetFrame++
            else {
                this.anim = 'box'
                this.targetFrame = this.frameMax
            }
        } else if(this.anim == 'fadeOut') {
            if ( this.targetFrame > 0)
                this.targetFrame--
            else {
                this.anim = 'none'
                return
            }
        }

        screen.printBox.drawBox(   screen.printBox.X + screen.printBox.Width/2  - this.aSizex[this.targetFrame]/2,
                                   screen.printBox.Y + screen.printBox.Height/2 - this.aSizey[this.targetFrame]/2,
                                   this.aSizex[this.targetFrame],
                                   this.aSizey[this.targetFrame]);

    },

    drawBox: function( x, y, sizex, sizey,select){

        select = (typeof select === "undefined") ? 0 : select;


        imgPrintSet = screen.printBox.imgPrintSet;

        s = screen['printBox']['printSet']

        if (select==0) {
            screen.printBox.drawElement(s['background'],x,y,sizex,sizey,imgPrintSet);
        }
        screen.printBox.drawElement(s['topLeftBox'],x,y,s['topLeftBox']['sizex'],s['topLeftBox']['sizey'],imgPrintSet,select);
        screen.printBox.drawElement(s['TopBox'],
                                    x+s['topLeftBox']['sizex'],y,
                                    sizex-s['topLeftBox']['sizex']-s['topRightBox']['sizex'],s['TopBox']['sizey'],
                                    imgPrintSet,select);
        screen.printBox.drawElement(s['topRightBox'],
                                    x+sizex-s['topRightBox']['sizex'],y,
                                    s['topRightBox']['sizex'],s['topRightBox']['sizey'],
                                    imgPrintSet,select);

        screen.printBox.drawElement(s['LeftBox'],
                                    x,y+s['topLeftBox']['sizey'],
                                    s['LeftBox']['sizex'], sizey-s['topLeftBox']['sizey']-s['bottomLeftBox']['sizey'],
                                    imgPrintSet,select);
        screen.printBox.drawElement(s['RightBox'],
                                    x+sizex-s['topRightBox']['sizex'],y+s['topRightBox']['sizey'],
                                    s['RightBox']['sizex'],sizey-s['topRightBox']['sizey']-s['bottomRightBox']['sizey'],
                                    imgPrintSet,select);

        screen.printBox.drawElement(s['bottomLeftBox'],
                                    x,y+sizey-s['bottomLeftBox']['sizey'],
                                    s['bottomLeftBox']['sizex'],s['bottomLeftBox']['sizey'],
                                    imgPrintSet,select);
        screen.printBox.drawElement(s['BottomBox'],
                                    x+s['bottomLeftBox']['sizex'],y+sizey-s['bottomRightBox']['sizey'],
                                    sizex-s['bottomLeftBox']['sizex']-s['bottomRightBox']['sizex'],s['BottomBox']['sizey'],
                                    imgPrintSet,select);
        screen.printBox.drawElement(s['bottomRightBox'],
                                    x+sizex-s['bottomRightBox']['sizex'],y+sizey-s['bottomRightBox']['sizey'],
                                    s['bottomRightBox']['sizex'],s['bottomRightBox']['sizey'],
                                    imgPrintSet,select);

    }

}

screen.effectPixelize2 = function(pixelation) {

    var imageData = this.ctx.getImageData(this.GSTARTX, this.GSTARTY, this.GWIDTH , this.GHEIGHT);
    var data = imageData.data;

    for(var y = 0; y < this.GHEIGHT; y += pixelation) {
        for(var x = 0; x < this.GWIDTH; x += pixelation) {
        var red = data[((this.GWIDTH * y) + x) * 4];
        var green = data[((this.GWIDTH * y) + x) * 4 + 1];
        var blue = data[((this.GWIDTH * y) + x) * 4 + 2];

            for(var n = 0; n < pixelation; n++) {
                for(var m = 0; m < pixelation; m++) {
                    if(x + m < this.GWIDTH) {
                        data[((this.GWIDTH * (y + n)) + (x + m)) * 4] = red;
                        data[((this.GWIDTH * (y + n)) + (x + m)) * 4 + 1] = green;
                        data[((this.GWIDTH * (y + n)) + (x + m)) * 4 + 2] = blue;
                    }
                }
            }
        }
    }
    this.ctx.putImageData(imageData, 0, 0)
};

screen.effectPixelize = function(pixelation) {
    this.ctx.drawImage(this.canvas, this.GSTARTX, this.GSTARTY,  this.GWIDTH , this.GHEIGHT,    this.GSTARTX, this.GSTARTY,    pixelation  ,   pixelation      )
    this.ctx.drawImage(this.canvas, this.GSTARTX, this.GSTARTY,   pixelation ,   pixelation,    this.GSTARTX, this.GSTARTY,    this.GWIDTH ,   this.GHEIGHT    )
};

screen.effectColor = function(opacity,color) {
	this.ctx.save()
	this.ctx.fillStyle = color;
	this.ctx.globalAlpha=opacity;
	this.ctx.fillRect(this.GSTARTX, this.GSTARTY, this.GWIDTH, this.GHEIGHT);
	this.ctx.restore()
};




screen.effects = {
    selected: null,
    startFrame: 0,
    endFrame: 0,
    intensity: [8,16,24,32,48,64,128],
    keepAfter: false,
    fadeIn: function(params) {
        var changeEffect = params[0]
        var shouldKeepAfter = params[1]
        screen.effects.startFrame = screen.frameCount;
        screen.effects.endFrame = screen.effects.intensity.length;
        screen.effects.selected = changeEffect;
        if (shouldKeepAfter =="keepEffect")
            screen.effects.keepAfter=true;
        else
            screen.effects.keepAfter=false;
    },
    fadeOut: function(params) {
        var changeEffect = params[0]
        var shouldKeepAfter = params[1]
        screen.effects.startFrame = screen.frameCount;
        screen.effects.endFrame = screen.effects.intensity.length;
        screen.effects.selected = changeEffect;
        if (shouldKeepAfter =="keepEffect") {
            screen.effects.keepAfter=true;
        } else
            screen.effects.keepAfter=false;
    },
    noEffect: function() {
       screen.effects.selected = null;
    }
};

screen.drawEffects = function(){
    if(screen.effects.selected == null) {
        return
    }
    if (screen.effects.selected == 'pixelizeFadeIn') {
        var frameToDraw = screen.frameCount-screen.effects.startFrame
        if (frameToDraw>= screen.effects.endFrame) {
            frameToDraw = screen.effects.endFrame-1
            if (!screen.effects.keepAfter)
                screen.effects.noEffect()
        }
        screen.effectPixelize(screen.effects.intensity[frameToDraw])
    }
    if (screen.effects.selected == 'pixelizeFadeOut') {
        var frameToDraw = screen.effects.endFrame-screen.frameCount+screen.effects.startFrame
        if (frameToDraw <= 0) {
            frameToDraw = 0
            if (!screen.effects.keepAfter)
                screen.effects.noEffect()
        }
        screen.effectPixelize(screen.effects.intensity[frameToDraw])
    }
	if (screen.effects.selected == 'blackFadeOut') {
		var frameToDraw = screen.frameCount-screen.effects.startFrame
		if (frameToDraw>= screen.effects.endFrame) {
			frameToDraw = screen.effects.endFrame-1
			if (!screen.effects.keepAfter)
				screen.effects.noEffect()
		}
		screen.effectColor(screen.effects.intensity[frameToDraw]/128,'#000000')
	}
	if (screen.effects.selected == 'blackFadeIn') {
		var frameToDraw = screen.effects.endFrame-screen.frameCount+screen.effects.startFrame
		if (frameToDraw <= 0) {
			frameToDraw = 0
			if (!screen.effects.keepAfter)
				screen.effects.noEffect()
		}
		screen.effectColor(screen.effects.intensity[frameToDraw]/128,'#000000')
	}
	if (screen.effects.selected == 'whiteFadeOut') {
		var frameToDraw = screen.frameCount-screen.effects.startFrame
		if (frameToDraw>= screen.effects.endFrame) {
			frameToDraw = screen.effects.endFrame-1
			if (!screen.effects.keepAfter)
				screen.effects.noEffect()
			}
			screen.effectColor(screen.effects.intensity[frameToDraw]/128,'#FFFFFF')
		}
		if (screen.effects.selected == 'whiteFadeIn') {
			var frameToDraw = screen.effects.endFrame-screen.frameCount+screen.effects.startFrame
			if (frameToDraw <= 0) {
				frameToDraw = 0
				if (!screen.effects.keepAfter)
					screen.effects.noEffect()
				}
				screen.effectColor(screen.effects.intensity[frameToDraw]/128,'#FFFFFF')
			}
};

function compareChars(a,b) {
    if(a.mapy == b.mapy)
    {
        return (a.mapx < b.mapx) ? -1 : (a.mapx > b.mapx) ? 1 : 0;
    }
    else
    {
        return (a.mapy < b.mapy) ? -1 : 1;
    }
}

camera.drawChars = function() {
    chars.sort(compareChars)
    var count = chars.length;
    for(var i = 0; i < count; i++) {
        var item = chars[i];
        camera.drawChar(item)
    }
}

screen.drawMenu = function(menu){
    var maxItems = menu.itemsLength
    var maxItemStringLength = menu.maxItemStringSize()


    screen.printBox.drawBox( menu['drawx'],
                             menu['drawy'] ,
                             menu['width'],
                             menu['height']);

    for( var i = 0; i < maxItems; i += 1){
        if( menu.items[Object.keys(menu.items)[i]].selected) {
            if ( menu.wait) {
            screen.printBox.drawBox( menu['drawx']+8,
                                     menu['drawy'] +8+32*i,
                                     menu['width']-16,
                                     32,
                                     1);
            } else {
            screen.printBox.drawBox( menu['drawx']+8,
                                     menu['drawy'] +8+32*i,
                                     menu['width']-16,
                                     32,
                                     1+Math.floor(screen.frameCount/4)%2);
            }

            if( typeof menu.items[Object.keys(menu.items)[i]].icon !== "undefined") {
                var imgPrintSet = screen.printBox.imgPrintSet;
                var s = screen['printBox']['printSet']
                var icon = s[menu.items[Object.keys(menu.items)[i]].icon]

                screen.printBox.drawBox( menu['drawx']+menu['width'],
                                         menu['drawy'] ,
                                         icon.sizex+16,
                                         icon.sizey+16);
                screen.printBox.drawElement(icon,menu['drawx']+menu['width']+8,menu['drawy']+8,icon.sizex,icon.sizey,imgPrintSet)
            }

        }
        screen.ctx.fillText(Object.keys(menu.items)[i], screen.GSTARTX+menu['drawx']+16,screen.GSTARTY+menu['drawy']+menu.items[Object.keys(menu.items)[i]].itemy);
    }

}


screen.loop = function(){

	try{

		// draw
		screen.frameCount += 1;
		screen.clearAll();

		if(!screen.paused){

			// update
			engine.update(screen.frameCount);
            camera.setupMap(this.engine.currentLevel)
            if(debug.showLayer.layer1)
			    camera.drawMapLayer(this.engine.currentLevel, "layer1");

            if(debug.showLayer.layer2)
			    camera.drawMapLayer(this.engine.currentLevel, "layer2");

            if(debug.showLayer.layer3)
                camera.drawChars();
    			//camera.drawChar(player);

            if(debug.showLayer.layer4)
    			camera.drawMapLayer(this.engine.currentLevel, "layer4");
            screen.drawEffects();
            screen.drawHID();


           for( var menuToDraw in menus.allMenus ) {
                if(menus.allMenus[menuToDraw].enabled) {
                    screen.drawMenu(menus.allMenus[menuToDraw]);
                }
            }

            screen.printBox.drawBoxAnimation();

			// updates
			printer.update();


		}

        debug.FPS.draw();
		screen.timer = setTimeout("screen.loop()", 1000/60.0);

	}catch(err){
		alert("loop error: "+err);
	}
}

debug = {};

debug.showLayer = {
    layer1 : true,
    layer2 : true,
    layer3 : true,
    layer4 : true
};

debug.FPS = {
    counter : 0,
    FPS : 0,
    show : false,
    draw : function(){
        this.counter += 1;
        if ( this.show ) {
            screen.ctx.fillText(this.FPS.toString()+" fps", screen.GSTARTX+2,screen.GSTARTY+16);
        }
    },
    loop : function(){
        this.FPS = this.counter;
        this.counter = 0;
        this.timer = setTimeout("debug.FPS.loop()", 1000);
    }


}

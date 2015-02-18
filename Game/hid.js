var HID = {
    scale: 1,
    bsz: 96,
    offset: 416,
    axeNotNull: 0.4,
    inputs:{
	    up:{
            letter: 'W',
		    active: false,
		    mapX: 96,
		    mapY: 0,
            color: '#111111',
            gamepad: function(pad){ return (pad.axes[1] < -HID.axeNotNull); }
	    },
	    left:{
            letter: 'A',
		    active: false,
		    mapX: 0,
		    mapY: 96,
            color: '#111111',
            gamepad: function(pad){ return (pad.axes[0] < -HID.axeNotNull); }
	    },
	    down:{
            letter: 'S',
		    active: false,
		    mapX: 96,
		    mapY: 192,
            color: '#111111' ,
            gamepad: function(pad){ return (pad.axes[1] > HID.axeNotNull); }
	    },
	    right:{
            letter: 'D',
		    active: false,
		    mapX: 192,
		    mapY: 96,
            color: '#111111' ,
            gamepad: function(pad){ return (pad.axes[0] > HID.axeNotNull); }
	    },
	    accept:{
            letter: 'I',
		    active: false,
		    mapX: 304,
		    mapY: 32,
            color: '#127826' ,
            gamepad: function(pad){ return pad.buttons[0].pressed; }
	    },
	    cancel:{
            letter: 'J',
		    active: false,
		    mapX: 304,
		    mapY: 160,
            color: '#ed1c24' ,
            gamepad: function(pad){ return pad.buttons[1].pressed; }
	    }
    },
    debugKeys: {
        resize: {
            letter: '0',
            toggle: function(){screen.resize()}
        },
        layer1: {
            letter: '1',
            toggle: function(){debug.showLayer.layer1 = !debug.showLayer.layer1}
        },
        layer2: {
            letter: '2',
            toggle: function(){debug.showLayer.layer2 = !debug.showLayer.layer2}
        },
        layer3: {
            letter: '3',
            toggle: function(){debug.showLayer.layer3 = !debug.showLayer.layer3}
        },
        layer4: {
            letter: '4',
            toggle: function(){debug.showLayer.layer4 = !debug.showLayer.layer4}
        }
    },


    processGamepad: function (){
        if (typeof HID.gamepads != 'undefined') {

            for (var i = 0; i < HID.gamepads.length; ++i)
            {
                var pad = HID.gamepads[i];

                for(var tag in HID.inputs){
                    var HIDItem = HID.inputs[tag];

                    if( HIDItem.gamepad(pad) ) {
                        HIDItem.active = true
                    } else
                        HIDItem.active = false
                }

            }
        }
    },

    clearInputs: function (){
	    for(var tag in HID.inputs){
		    var HIDItem = HID.inputs[tag];
		    HIDItem.release = false;
	    }
    },

    cleanInputs: function (){
	    for(var tag in HID.inputs){
		    var HIDItem = HID.inputs[tag];
		    HIDItem.active = false;
	    }
    },

    log: function(text){
	    var tag = document.getElementById("log");
	    tag.innerHTML = text;
    },

    keyDown: function (e){
	    var evtobj = window.event ? event : e ;
	    var unicode = evtobj.charCode ? evtobj.charCode : evtobj.keyCode;
	    var actualkey = String.fromCharCode(unicode);

        for(var key in HID.inputs){
            var HIDItem = HID.inputs[key];

            if(actualkey == HIDItem.letter){
                HIDItem.active = true;
            }
        }

    },

    keyUp: function (e){
	    var evtobj = window.event ? event : e ;
	    var unicode = evtobj.charCode ? evtobj.charCode : evtobj.keyCode;
	    var actualkey = String.fromCharCode(unicode);

        for(var key in HID.inputs){
            var HIDItem = HID.inputs[key];

            if(actualkey == HIDItem.letter){
                HIDItem.active = false;
            }
        }

        for(var key in HID.debugKeys){
            var HIDItem = HID.debugKeys[key];

            if(actualkey == HIDItem.letter){
                HIDItem.toggle();
            }
        }

    },

    setupTouchZone: function (_screen){
        this.screen = _screen
        this.touchzone = this.screen.canvas
    },

    setupKeyboardListeners: function (){
	    document.onkeydown = HID.keyDown;
	    document.onkeyup = HID.keyUp;
    },

    handleTouchDown: function (evnt){
        evnt.preventDefault();
	    HID.processTouches(event.touches, "down");
    },

    handleTouchMove: function (evnt){
        evnt.preventDefault();
	    HID.processTouches(event.touches, "move");
    },

    handleTouchUp: function (evnt){
        evnt.preventDefault();
	    HID.processTouches(event.touches, "up");
    },

    processTouches: function (touches, kind){
	    //HID.log("type:" +kind+" seed: "+Date());
	    for(var tag in HID.inputs){

		    var HIDItem = HID.inputs[tag];
		    var touched = false;

            var offsetTop = this.screen.canvas.offsetTop,
                offsetLeft = this.screen.canvas.offsetLeft;
                scale = this.screen.currentWidth / this.screen.WIDTH;


		    for(var i = 0; i < touches.length; i++){

		        var position = {x:((touches[i].pageX-offsetLeft)/scale),
						        y:((touches[i].pageY-offsetTop)/scale)};



			    if(position.x > HIDItem.mapX && position.y > this.offset+HIDItem.mapY){
				    if(position.x < HIDItem.mapX+this.bsz  && position.y < this.offset+HIDItem.mapY+this.bsz){
					    touched = true;
				    }
			    }

		    }

		    if(touched){
			    HIDItem.active = true;
			    if(kind == "down"){
				    HIDItem.release = true;
			    }
		    }else{
			    HIDItem.active = false;
		    }

	    }

        for(var menuTag in menus.allMenus) {
            var aMenu = menus.allMenus[menuTag]

            if(aMenu.enabled && !aMenu.wait) {
                var maxItems = aMenu.itemsLength

                for( var menuItemTag in aMenu.items){
                    var menuItem = aMenu.items[menuItemTag];
            		var touched = false;

                    var offsetTop = this.screen.canvas.offsetTop,
                        offsetLeft = this.screen.canvas.offsetLeft;
                        scale = this.screen.currentWidth / this.screen.WIDTH;


                    for(var i = 0; i < touches.length; i++){

                        var position = {x:((touches[i].pageX-offsetLeft)/scale),
				                        y:((touches[i].pageY-offsetTop)/scale)};



	                    if(position.x > (screen.GSTARTX+aMenu.drawx) && position.y > (screen.GSTARTY+aMenu.drawy+menuItem.itemy-32)){
		                    if(position.x < (screen.GSTARTX+aMenu.drawx+aMenu.width) && position.y < (screen.GSTARTY+aMenu.drawy+menuItem.itemy)){
			                    touched = true;}}

                    }

		            if(touched){
            			if(kind == "down" && menuItem.selected){
				            HID.inputs["accept"].active = true
                            return;
			            }
                        for( var z = 0; z < maxItems; z += 1) {
                            aMenu.items[Object.keys(aMenu.items)[z]].selected = false
                        }
			            menuItem.selected = true
                        aMenu.selectedItem = menuItem
		            }

                }


            }
        }

    },

    setupListeners: function(){
	    window.addEventListener('touchstart', HID.handleTouchDown, false);
        window.addEventListener('touchmove', HID.handleTouchMove, false);
	    window.addEventListener('touchend', HID.handleTouchUp, false);
        window.addEventListener("gamepadconnected", function(e) {
            HID.gamepads = navigator.getGamepads();
            actions.alert("gamepad connected!")
        });
        window.addEventListener("gamepaddisconnected", function(e) {
            HID.gamepads = [];
            HID.cleanInputs();
            HID.clearInputs();
            actions.alert("gamepad disconnected.")
        });

    },

    setup: function(screentosetup){
        this.setupTouchZone(screentosetup);
        this.setupListeners();
        this.setupKeyboardListeners();
    }

};

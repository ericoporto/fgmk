var menus = {
    allMenus : [],
    isAnyMenuEnabled : function() {
        var returnValue = false
        for(var _menu in this.allMenus) {
            if(this.allMenus[_menu].enabled) {
                returnValue = true;
            }
        }
        return returnValue;
    },
    updateMenuEnabled : function() {
        var returnValue = null
        for(var _menu in this.allMenus) {
            if(this.allMenus[_menu].enabled) {
                this.allMenus[_menu].update();
            }
        }
        return returnValue;
    },
    setParent : function(o){
        if(o.items != undefined){
            for(n in o.items){
                o.items[n].parent = o;
                this.setParent(o.items[n]);
            }
        }
    },
    setDrawables : function(menuToDraw) {
        if (menuToDraw.parent == null) {
            menuToDraw['drawx'] = 16 ;
            menuToDraw['drawy'] = 16 ;
            menuToDraw['height'] = menuToDraw.itemsLength*32+32 ;
            menuToDraw['width'] =  menuToDraw.maxItemStringSize()*13+32 ;
        } else {
            menuToDraw['drawx'] = menuToDraw.parent.drawx+menuToDraw.parent.width ;
            menuToDraw['drawy'] = menuToDraw.parent.drawy ;
            menuToDraw['height'] = menuToDraw.itemsLength*32+32 ;
            menuToDraw['width'] =  menuToDraw.maxItemStringSize()*13+32 ;
        }
    },
    setAllDrawables : function() {
        for( var anotherMenu in this.allMenus ) {
            for( var aMenu in this.allMenus ) {
                this.setDrawables(this.allMenus[aMenu]);
            }
        }
    }
};

function menu(_items, _index, _noexit) {

    var tempArray = [];

    _index = (typeof _index === "undefined") ? null : _index;
    _noexit = (typeof _noexit === "undefined") ? false : true;
    this.items=_items;
    this.noexit=_noexit;

    this.parent = null
    this.index = _index
    this.enabled=false;
    this.selectedItem=null;
    this.wait = false
    this.isMenu = true;

    this.updateOrder = function(){

        for (var i = 0; i < Object.keys(this.items).length; i++) {
            var _itemKey = Object.keys(this.items)[i];

            tempArray[i] = [_itemKey, this.items[_itemKey].index]

        }
        tempArray.sort(function(a, b) {return a[1] - b[1]})

        this.selectedItem = this.items[tempArray[0][0]]

        for (var i = 0; i < tempArray.length; i++) {

            if ( i == 0) {
                this.items[tempArray[i][0]].previous = tempArray[0][0]
                this.items[tempArray[i][0]].next = tempArray[i+1][0]
            } else if (i == tempArray.length-1) {
                this.items[tempArray[i][0]].previous = tempArray[i-1][0]
                this.items[tempArray[i][0]].next = tempArray[i][0]
            } else {
                this.items[tempArray[i][0]].previous = tempArray[i-1][0]
                this.items[tempArray[i][0]].next = tempArray[i+1][0]
            }

            this.items[tempArray[i][0]].itemy = 32+i*32

        }

        if(this.selectedItem == null)
            this.selectedItem = this.items[Object.keys(this.items)[0]]


            this.selectedItem.selected = true

        }

        this.updateOrder()

        this.maxItemStringSize = function() {
            var returnValue = 0

            for (var i = 0; i < Object.keys(this.items).length; i++) {
                var _itemKey = Object.keys(this.items)[i];


                if ( returnValue < _itemKey.length) {
                    returnValue = _itemKey.length;
                }
            }

            return returnValue
        };

        this.itemsLength = Object.keys(_items).length

        this.exit= function(){
            this._counter = 0;
            this.enabled = false;
            HID.inputs["cancel"].active = false;
            engine.waitTime(200)

            if(this.parent!=null) {
                this.parent.wait = false;
                this.parent.menuKeyWasPressed=32
            } else {
                engine.atomStack.push(engine.atomStack.push([function(){engine.atomStack = menus.holdAtomStack },'']),'')
            }
        };
        this.activate= function(){
            this.enabled = true ;
            if(this.parent!=null) {
                this.parent.wait = true;
            } else {
                menus.holdAtomStack = engine.atomStack
                engine.atomStack=new Array();
            }
        };
        this._counter=0; //this counter is here to solve a bug with the gamepad cancel button
        this.menuKeyWasPressed=0;
        this.update= function(){
            if(this._counter < 20)
                this._counter+=1;

                if(this.menuKeyWasPressed==0) {
                    if(!this.wait) {
                        if(HID.inputs["up"].active){
                            this.selectedItem.selected = false
                            this.selectedItem = this.items[this.selectedItem.previous]
                            this.selectedItem.selected = true
                            HID.inputs["up"].active = false
                            this.menuKeyWasPressed=32
                        }else if(HID.inputs["left"].active){


                        }else if(HID.inputs["right"].active){


                        }else if(HID.inputs["down"].active){
                            this.selectedItem.selected = false
                            this.selectedItem = this.items[this.selectedItem.next]
                            this.selectedItem.selected = true
                            HID.inputs["down"].active = false
                            this.menuKeyWasPressed=32
                        }else if(HID.inputs["accept"].active){

                            HID.inputs["accept"].active = false
                            if (this.selectedItem.action == 'exit') {
                                this.exit();
                            } else if ( Object.prototype.toString.call(this.selectedItem.action) === '[object Array]') {
                                for(var i=0; i < this.selectedItem.action.length; i++) {
                                    if ( this.selectedItem.action[i] == 'exit') {
                                        this.exit()
                                    } else if ( this.selectedItem.action[i] == 'goWait') {
                                        engine.atomStack.push([function(){this.wait = true;},'']);
                                    } else if ( this.selectedItem.action[i] == 'stopWait') {
                                        engine.atomStack.push([function(){this.wait = false;},'']);
                                    } else {
                                        this.selectedItem.action[i]();
                                    }
                                }
                            } else {
                                if( typeof this.selectedItem.isMenu === "undefined") {
                                    this.selectedItem.action();
                                } else {
                                    this.selectedItem.menuKeyWasPressed=32
                                    this.selectedItem.action();
                                }
                            }
                            this.menuKeyWasPressed=32
                        }else if(HID.inputs["cancel"].active){
                            if(this._counter >= 20 && this.noexit == false) {
                                HID.inputs["cancel"].active = false
                                this.exit()
                                engine.waitTime(200)
                                this.menuKeyWasPressed=32
                            }
                        }
                    }
                } else {
                    this.menuKeyWasPressed-=4
                }
            };

            this.action = this.activate;
            this.mdelete = function(){
                for (var i = 0; i < menus.allMenus.length; i++) {
                    if(menus.allMenus[i] == this){
                        menus.allMenus.splice(i,1)
                        break
                    }
                }

            }

            menus.allMenus.push(this);

        };
        

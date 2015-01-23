items = {}
items.setup = function (itemsjson){
    this.inventory = {}
    this.allitems = {}
    this.allitems = itemsjson
    this.defaultItem = function(){
        return {
            "equipable":false,
            "equiped":false,
            "usable":false,
            "unique":false,
            "effect":null,
            "staticModifier":null,
            "description":false,
            "name":null,
            "icon":null,
            "quantity":1
        }
    }
    this.addItem = function(itemname){
        if(itemname in this.inventory){
            if(!(this.inventory[itemname].unique)) {
                this.inventory[itemname].quantity += 1
            }
        } else if(itemname in this.allitems){
            var item = this.defaultItem()
            //merges the item to default item.
            //since copy is shallow, won't duplicate extensive items
            for (var key in this.allitems[itemname]) {
                 item[key] = this.allitems[itemname][key];
            }
            if(item["name"] == null){
                item["name"] = itemname
            }

            this.inventory[itemname] = item

        }
        this.menuUpdate(engine.mapMenu)
    }
    this.subtractItem = function(itemname){
        this.inventory[itemname].quantity -= 1
        if(this.inventory[itemname].quantity <= 0){
            this.deleteItem(itemname)
        }

        this.menuUpdate(engine.mapMenu)
    }

    this.deleteItem = function(itemname){
        delete this.inventory[itemname]
    }

    this.useItem = function(itemname){

    }

    this.equipItem = function(itemname){

    }

    this.unequipItem = function(itemname){

    }

    this.lookItem = function(itemname){

    }

    this.dropItem = function(itemname){

    }

    this.getMenu = function(){
        return this.menu
    }

    this.menuUpdate = function(mapmenu){
        if(!(typeof this.menu === "undefined")){
            this.menu.delete()
        } else {
            this.menu = {}
        }

        var items2add = {}
        var i=0
        for(var iitem in this.inventory){
            var item = this.inventory[iitem].name

            var k=0
            var itemactions = {}

            if(this.inventory[iitem].equipable){
                if(this.inventory[iitem].equiped) {
                    itemactions["unequip"] = {}
                    itemactions["unequip"]["index"] = k
                    itemactions["unequip"]["action"] = [function(){ items.unequipItem(iitem) }, 'exit']
                } else {
                    itemactions["equip"] = {}
                    itemactions["equip"]["index"] = k
                    itemactions["equip"]["action"] = [function(){ items.equipItem(iitem) }, 'exit']
                }
                k++
            }
            if(this.inventory[iitem].usable){
                itemactions["use"] = {}
                itemactions["use"]["index"] = k
                itemactions["use"]["action"] = [function(){ items.useItem(iitem) }, 'exit']
                k++
            }
            if(this.inventory[iitem].description){
                itemactions["look"] = {}
                itemactions["look"]["index"] = k
                itemactions["look"]["action"] = [function(){ items.lookItem(iitem) }, 'exit']
                k++
            }
            if(!(this.inventory[iitem].unique)){
                itemactions["drop"] = {}
                itemactions["drop"]["index"] = k
                itemactions["drop"]["action"] = [function(){ items.dropItem(iitem) }, 'exit']
                k++
            }

            itemactions["back"] = {}
            itemactions["back"]["action"] = 'exit'
            itemactions["back"]["index"] = k++

            items2add[item] = new menu(itemactions, i)


            i++
        }

        if(i == 0){
            items2add["empty"] = {}
            items2add["empty"]["action"] = function(){}
            items2add["empty"]["index"] = i
            i++
        }

        items2add["back"] = {}
        items2add["back"]["action"] = 'exit'
        items2add["back"]["index"] = i
        i++


        this.menu = new menu(items2add, 0)
        if(typeof mapmenu === "undefined"){
            menus.setParent(this.menu);
        } else {
            mapmenu.items.items = this.menu
            mapmenu.updateOrder()
            menus.setParent(mapmenu);
        }

        menus.setAllDrawables()
    }

}

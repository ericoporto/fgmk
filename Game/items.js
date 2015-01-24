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
            "statMod":null,
            "description":false,
            "name":null,
            "icon":null,
            "category":null,
            //common category are armor, weapon, ...
            "action":null,
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
        if(this.inventory[itemname].action == null){

        }
    }

    this.equipItem = function(itemname){
        if(player.party.length == 1){
            var currHero = battle.heroes[player.party[0]]
            var heroname = player.party[0]
            var eq_item = this.inventory[itemname]
            if(currHero.equiped[eq_item.category]){

            } else {
                eq_item.equiped = heroname
                currHero.equiped[eq_item.category] = itemname
                if(eq_item.statMod){
                    currHero.mod.w += eq_item.statMod.w
                    currHero.mod.r += eq_item.statMod.r
                    currHero.mod.m += eq_item.statMod.m
                }
            }
        }

        this.menuUpdate(engine.mapMenu)
    }

    this.unequipItem = function(itemname){
        if(player.party.length == 1){
            var currHero = battle.heroes[player.party[0]]
            var heroname = player.party[0]
            var eq_item = this.inventory[itemname]
            if(currHero.equiped[eq_item.category] == itemname && eq_item.equiped == heroname){
                if(eq_item.statMod){
                    currHero.mod.w -= eq_item.statMod.w
                    currHero.mod.r -= eq_item.statMod.r
                    currHero.mod.m -= eq_item.statMod.m
                }
                eq_item.equiped = false
                currHero.equiped[eq_item.category] = false
            } else {
                console.log("tried to unequip item, but it wasn't equiped!")
            }
        }

        this.menuUpdate(engine.mapMenu)
    }

    this.lookItem = function(itemname){
        if(this.inventory[itemname].description){
            actions.showText(this.inventory[itemname].description)
        }
    }

    this.dropItem = function(itemname){
        this.subtractItem(itemname)

        //will update on subtract
    }

    this.getMenu = function(){
        return this.menu
    }

    this.menuUpdate = function(mapmenu){
        if(!(typeof this.menu === "undefined")){
            var wasenable = this.menu.enabled
            this.menu.enabled = false
            this.menu.delete()
        } else {
            var wasenable = false
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

        this.menu.enabled = wasenable

    }

}

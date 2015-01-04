var title = {};

title.setup = function(){
    title.startMenu = new menu({
        start: {
            action: [function(){ actions.showText("let's play!");
                        actions.fadeOut("blackFadeOut;keepEffect");
                        actions.changeState("map") },
                    'exit',
                    function(){actions.stopPicture("")},
                    function(){actions.fadeIn("blackFadeIn;doNotKeep")}],
                index: 0
            },
        exit: {
                action: 'exit',
                index: 1
            }
        });
    menus.setParent(title.startMenu);
    title.startMenu.activate()
    actions.showPicture("title;0;0")
}

title.startScreen = function(){
     title.update()
}

title.update = function(){
    if(printer.isShown)
        return;

    if(player.steps == 0){
        if(HID.inputs["cancel"].active){
            HID.inputs["cancel"].active = false
            title.startMenu.activate()
        }
    }
};

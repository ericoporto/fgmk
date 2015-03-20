feedbackEng = {}

feedbackEng.setup = function() {
    this.once = false,
    this.timer = null,
    this.vibrationOn = false,
    this.soundOn = false;
    this.flist= {};
    this.loadedSounds = {};
    this.vibrate= null;

    this.flist = resources.feedback
    navigator.vibrate = navigator.vibrate || navigator.webkitVibrate || navigator.mozVibrate || navigator.msVibrate;
    if (navigator.vibrate) {
        // vibration API supported
        this.vibrationOn = true ;
    }
    if(window.isFirefox()) {
        this.soundOn = true;
    }
    for (var sound in this.flist) {
        this.loadedSounds[sound] =  document.getElementById(this.flist[sound].s)
    }
};

feedbackEng.play = function(feedback) {
    if (this.once == false) {
        if(this.vibrationOn) {
            navigator.vibrate(this.flist[feedback].v);
        }
        if(this.soundOn) {
            this.loadedSounds[feedback].cloneNode(true).play();
        }
        //this.once = true;
        //this.turnOnceOffTime();
    }
};


feedbackEng.turnOnceOffTime =function() {
    this.timer = setTimeout(function() {
        feedbackEng.once = false;
    }, 100.0);
};

bgmusic = {
    setup: function(){

    },
    play: function(){

    }
}

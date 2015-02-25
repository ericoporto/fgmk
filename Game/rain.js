function rain(__context, __width,__height, ___screen){
    var that = this;

    var ___context = __context
    var rainBufferCanvas = null;
    var rainBufferCanvasCtx = null;
    var particles = [];
    var removeparticles = [];
    var RainDropTimer = null;
    var stop = false;
    var colors = [];
    var rainBufferWidth = (typeof __width === "undefined") ? 416 : __width;
    var rainBufferHeight = (typeof __height === "undefined") ? 416 : __height;

    this.raining = false;

    function toColor(num) {
        var g = Math.min(Math.round(num), 0xFF);
        return "rgba(" + [g, g, g].join(",") + ",1)";
    };
    function addRainDrop() {
        particles[particles.length] = new RainDrop();
        if (particles.length == that.maxRainDrops)
            clearInterval(RainDropTimer);
        };

        this.startRain = function() {

            for(var i=0; i<7; i++) {
                colors[i]=toColor((i)*128/6+128);
            }
            that.raining = true
            stop = false
            that.maxRainDrops = 200;

            rainBufferCanvas = document.createElement("canvas");
            rainBufferCanvasCtx = rainBufferCanvas.getContext("2d");
            rainBufferCanvasCtx.mozImageSmoothingEnabled = false;
            rainBufferCanvasCtx.canvas.width = rainBufferWidth;
            rainBufferCanvasCtx.canvas.height = rainBufferHeight;

            RainDropTimer = setInterval(addRainDrop, 200);
        };

        this.stopRain = function() {
            stop = true;
            clearInterval(RainDropTimer);
        };


        function blankRainBC() {
            var npart = particles.length
            rainBufferCanvasCtx.clearRect(0, 0, rainBufferCanvasCtx.canvas.width, rainBufferCanvasCtx.canvas.height);
            if(npart > 50) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.2)";
            } else if(npart > 35) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.15)";
            } else if(npart > 25) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.1)";
            } else if(npart > 20) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.075)";
            } else if(npart > 15) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.05)";
            } else if(npart > 10) {
                rainBufferCanvasCtx.fillStyle = "rgba(0,0,25,0.025)";
            }
            if(npart > 10) {
                rainBufferCanvasCtx.fillRect(0, 0, rainBufferCanvasCtx.canvas.width, rainBufferCanvasCtx.canvas.height);
            }
        };

        function DrawRainColor(colori){
            rainBufferCanvasCtx.beginPath();
            for (var i = 0; i < particles.length; i++) {
                if(colori==particles[i].color){
                    rainBufferCanvasCtx.moveTo(particles[i].x, particles[i].y);
                    rainBufferCanvasCtx.lineTo(particles[i].x+particles[i].width, particles[i].y+particles[i].height);
                }
            }
            rainBufferCanvasCtx.strokeStyle = colors[colori];
            rainBufferCanvasCtx.stroke();
        };

        this.DrawRain = function() {

            if(that.raining){

                for (var i = 0; i < particles.length; i++) {
                    if (particles[i].y < rainBufferHeight) {
                        particles[i].y += particles[i].speed;
                        if (particles[i].y >= rainBufferHeight) {
                            particles[i].y = -5;
                            if(stop) {
                                removeparticles.push(i)
                            }
                        }
                        particles[i].x += particles[i].drift;
                        if (particles[i].x > rainBufferWidth) {
                            particles[i].x = 0;
                            if(stop) {
                                removeparticles.push(i)
                            }
                        }
                    }
                }

                if(particles.length>0){
                    blankRainBC();

                    for (var k = 2; k< 6; k++){
                        DrawRainColor(k)
                    }

                    ___context.drawImage(rainBufferCanvas, ___screen.GSTARTX, ___screen.GSTARTY, rainBufferWidth, rainBufferHeight);
                }

                if(removeparticles.length > 0 ){
                    removeparticles.sort(function(a,b){ return b - a; });
                    while (removeparticles.length > 0){
                        particles.splice(removeparticles.pop(),1);
                    }
                    if(particles.length == 0){
                        that.raining = false
                    }
                }
            }
        };

        function RainDrop() {
            var angle = 2

            this.x = Math.round(Math.random() *rainBufferWidth);
            this.y = -10;
            this.drift = Math.round(Math.random() * 4) + 2;
            this.speed = this.drift*angle
            this.width = 8;
            this.height = 8*angle;
            this.color = this.drift
        }
    }

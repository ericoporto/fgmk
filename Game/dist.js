var dist = {}
dist.setup = function (viewCanvas, backgroundImage, alpha) {
    dist.alpha = alpha
    dist.tickssy = 0
    dist.bfx = {}
    dist.efnumb= []
    dist.efnumb[0] = 1
    dist.bfx.effectsrom = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,1,0,4,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,4,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,4,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,4,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,3,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,3,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,3,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,3,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,1,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,1,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,1,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,1,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,4,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,1,0,2,255,255,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,4,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,4,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,4,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,4,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,3,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,3,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,3,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,3,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,1,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,1,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,1,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,1,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,4,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,2,0,2,255,255,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,3,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,3,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,3,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,3,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,1,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,1,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,1,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,1,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,2,255,255,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,4,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,4,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,4,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,4,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,3,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,3,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,3,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,3,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,1,0,8,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,1,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,1,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,1,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,4,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,0,128,0,0,0,0,0,0,0,2,0,0,],
    [0,0,4,0,2,255,255,0,0,0,0,0,0,0,2,0,0,],
    [120,0,4,0,2,0,32,0,0,0,0,0,0,1,10,0,0,],
    [120,0,1,0,2,0,32,0,0,0,0,0,0,1,10,0,0,],
    [120,0,2,0,2,0,32,0,0,0,0,0,0,1,10,0,0,],
    [120,0,3,0,2,0,32,0,0,0,0,0,0,1,10,0,0,],
    [255,0,3,0,2,0,0,0,0,0,0,0,0,1,0,0,0,],
    [255,0,3,0,2,0,255,0,0,0,0,0,0,255,0,0,0,],
    [255,0,1,0,2,0,0,0,0,0,0,0,0,1,0,0,0,],
    [255,0,1,0,2,0,255,0,0,0,0,0,0,255,0,0,0,],
    [0,0,3,0,2,0,128,0,0,2,0,0,0,0,0,0,0,],
    [0,0,3,0,2,0,128,0,128,0,0,0,0,0,0,0,0,],
    [0,1,3,0,4,0,64,0,0,1,0,0,0,0,0,2,0,],
    [0,1,3,0,4,0,64,0,0,3,0,0,0,0,0,254,255,],
    [0,4,1,0,8,0,64,128,0,0,254,255,0,0,1,0,0,],
    [0,4,1,0,0,0,64,128,0,0,2,0,0,0,255,0,0,],
    [88,2,3,0,0,0,0,0,0,1,0,0,0,0,0,3,0,],
    [88,2,3,0,0,0,0,0,8,8,0,0,0,0,0,253,255,],
    [0,2,3,0,0,0,0,0,0,2,0,0,0,0,0,255,255,],
    [0,2,3,0,0,0,0,0,0,0,0,0,0,0,0,1,0,],
    [240,0,3,0,0,0,0,0,224,2,0,0,0,0,0,254,255,],
    [240,0,3,0,0,0,0,0,0,0,0,0,0,0,0,2,0,],
    [240,0,1,0,4,0,128,1,0,0,254,255,156,255,1,0,0,],
    [240,0,1,32,2,64,34,241,0,0,2,0,100,0,255,0,0,],
    [0,1,4,0,2,0,64,2,0,1,2,0,0,0,1,2,0,],
    [0,1,4,0,4,0,64,2,0,3,254,255,0,0,255,254,255,],
    [0,0,1,128,0,0,8,1,0,0,0,0,0,0,0,0,0,],
    [0,1,1,0,4,0,0,2,0,0,0,0,128,0,0,0,0,],
    [0,1,1,0,4,0,128,2,0,0,0,0,128,255,0,0,0,],
    [244,1,1,0,2,0,0,2,0,0,0,0,128,0,0,0,0,],
    [244,1,1,0,2,0,250,2,0,0,0,0,128,255,0,0,0,],
    [244,1,1,0,2,0,0,10,0,0,0,0,80,0,0,0,0,],
    [244,1,1,0,2,64,156,10,0,0,0,0,176,255,0,0,0,],
    [240,0,3,0,2,0,8,2,0,0,0,0,0,0,0,1,0,],
    [224,1,3,0,2,0,8,2,0,240,0,0,0,0,0,254,255,],
    [240,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
    [180,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
    [104,1,1,0,1,0,0,2,0,0,0,0,128,0,0,0,0,],
    [104,1,1,0,1,0,0,2,0,0,0,0,64,0,0,0,0,],
    [0,0,2,0,16,128,250,10,0,0,0,0,0,0,0,0,0,],
    [224,1,2,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [240,0,1,0,2,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,224,0,0,16,0,0,0,0,0,0,0,2,0,0,],
    [0,1,3,0,4,0,0,2,0,0,0,0,128,0,0,0,0,],
    [0,1,3,0,4,0,128,2,0,0,0,0,128,255,0,0,0,],
    [224,1,3,0,2,0,4,2,0,1,0,0,0,0,0,2,0,],
    [224,1,3,0,2,0,4,2,192,4,0,0,0,0,0,254,255,],
    [0,0,3,0,3,0,64,0,0,0,0,0,0,0,2,0,0,],
    [0,0,3,0,4,0,32,0,0,0,0,0,0,0,2,0,0,],
    [0,1,3,0,4,0,0,2,0,0,0,0,128,0,0,0,0,],
    [0,1,3,0,4,0,128,2,0,0,0,0,128,255,0,0,0,],
    [0,1,3,0,4,0,0,2,0,0,0,0,150,0,0,0,0,],
    [0,1,3,0,4,0,150,2,0,0,0,0,106,255,0,0,0,],
    [104,1,4,0,1,0,0,0,0,0,0,0,60,0,2,0,0,],
    [104,1,4,0,1,96,84,0,0,0,0,0,196,255,2,0,0,],
    [0,0,3,0,1,0,4,0,0,0,0,0,0,0,2,0,0,],
    [240,0,4,0,1,0,0,0,0,0,0,0,90,0,2,0,0,],
    [240,0,4,0,1,96,84,0,0,0,0,0,166,255,2,0,0,],
    [254,1,3,0,2,0,0,0,0,0,0,0,128,0,0,0,0,],
    [254,1,3,0,2,0,255,0,0,0,0,0,128,255,0,0,0]]

    dist.bfx.w = 256
    dist.bfx.h = 240

    dist.buffer = document.createElement('canvas');
    dist.buffer.width = dist.bfx.w;
    dist.buffer.height = dist.bfx.h;
    dist.bufferwidth = dist.buffer.width
    dist.bufferheight = dist.buffer.height
    dist.bctx = dist.buffer.getContext('2d');
    dist.bgimage = document.getElementById(backgroundImage);
    dist.bctx.drawImage(dist.bgimage,0,0,416,416,0,0,dist.bfx.w,dist.bfx.h)

    dist.bufferData = dist.bctx.getImageData(0, 0, dist.bfx.w, dist.bfx.h);
    dist.bdata = dist.bufferData.data;

    dist.bctx.mozImageSmoothingEnabled = false;
    dist.bctx.webkitImageSmoothingEnabled = false;
    dist.bctx.imageSmoothingEnabled = false;

    //this is the presentation canvas, the one the user sees
    dist.visible = viewCanvas
    dist.fctx = dist.visible.getContext('2d');
    dist.fctx.mozImageSmoothingEnabled = false;
    dist.fctx.webkitImageSmoothingEnabled = false;
    dist.fctx.imageSmoothingEnabled = false;

    dist.bfx.getType = function() {
        return dist.bfx.effect[2];
      };
    dist.bfx.getDuration = function() {
        return (dist.bfx.effect[0] + (dist.bfx.effect[1] << 8));
      }
    dist.bfx.getFrequency = function() {
        return (dist.bfx.effect[3] + (dist.bfx.effect[4] << 8));
      }
    dist.bfx.getAmplitude = function() {
        return (dist.bfx.effect[5] + (dist.bfx.effect[6] << 8));
      }
    dist.bfx.getCompression = function() {
        return (dist.bfx.effect[8] + (dist.bfx.effect[9] << 8));
      }
    dist.bfx.getFrequencyAcceleration = function() {
        return (dist.bfx.effect[10] + (dist.bfx.effect[11] << 8));
      }
    dist.bfx.getAmplitudeAcceleration = function() {
        return (dist.bfx.effect[12] + (dist.bfx.effect[13] << 8));
      }
    dist.bfx.getSpeed = function() {
        return dist.bfx.effect[14];
      }
    dist.bfx.getCompressionAcceleration = function() {
        return (dist.bfx.effect[15] + (dist.bfx.effect[16] << 8));
      }



    dist.Distorter = function(y, t, distortEffect, ampl, ampl_accel, s_freq, s_freq_accel, compr, compr_accel, speed) {
        // N.B. another discrepancy from Java--these values should be "short," and
        // must have a specific precision. this seems to effect backgrounds with
        // distortEffect == 1
        var C1 = (1 / 512.0).toFixed(6);
        var C2 = (8.0 * Math.PI / (1024 * 256)).toFixed(6);
        var C3 = (Math.PI / 60.0).toFixed(6);

        // Compute "current" values of amplitude, frequency, and compression
        var amplitude = (ampl + ampl_accel * t * 2);
        var frequency = (s_freq + s_freq_accel * t * 2);
        var compression = (compr + compr_accel * t * 2);

        // Compute the value of the sinusoidal line offset function
        var S = Math.round(C1 * amplitude * Math.sin((C2 * frequency * y + C3 * speed * t).toFixed(6)));

        if (distortEffect == 1) {
            return S;
        } else if (distortEffect == 2) {
            return (y % 2) == 0 ? -S : S;
        } else if (distortEffect == 3) {
            var L = Math.floor(y * (1 + compression / 256.0) + S) % 256;
            if (L < 0) L = 256 + L;
            if (L > 255) L = 256 - L;

            return L;
        }

        return 0;
    }

    dist.ComputeFrame = function(dst, src, distortEffect, letterbox, ticks, alpha, erase, ampl, ampl_accel, s_freq, s_freq_accel, compr, compr_accel, speed) {
        var bdst = dst;
        var bsrc = src;

        // TODO: hardcoing is bad.
        var dstStride = 1024;
        var srcStride = 1024;

        var x = 0, y = 0;

        for (y = 0; y < 224; y++)
        {
            S = dist.Distorter(y, ticks, distortEffect, ampl, ampl_accel, s_freq, s_freq_accel, compr, compr_accel, speed);
            L = y;

            if (distortEffect == 3) {
                L = S;
            }

            for (x = 0; x < 256; x++)
            {
                var bpos = x * 4 + y * dstStride;
                if (y < letterbox || y > 224 - letterbox)
                {
                    bdst[bpos + 2 ] = 0;
                    bdst[bpos + 1 ] = 0;
                    bdst[bpos + 0 ] = 0;
                    continue;
                }
                var dx = x;

                if (distortEffect == 1
                        || distortEffect == 2)
                {
                    dx = (x + S) % 256;
                    if (dx < 0) dx = 256 + dx;
                    if (dx > 255) dx = 256 - dx;
                }

                var spos = dx * 4 + L * srcStride;

                // Either copy or add to the destination bitmap
                if (erase == 1)
                {
                    bdst[bpos + 3 ] = 255;
                    bdst[bpos + 2 ] = (alpha * bsrc[spos + 2 ]);
                    bdst[bpos + 1 ] = (alpha * bsrc[spos + 1 ]);
                    bdst[bpos + 0 ] = (alpha * bsrc[spos + 0 ]);
                }
                else
                {
                    bdst[bpos + 3 ] = 255;
                    bdst[bpos + 2 ] += (alpha * bsrc[spos + 2 ]);
                    bdst[bpos + 1 ] += (alpha * bsrc[spos + 1 ]);
                    bdst[bpos + 0 ] += (alpha * bsrc[spos + 0 ]);
                }
            }
        }

        return bdst;
    }

    dist.test = function(effs){
        dist.tickssy+=1

        var blankcanvas = document.createElement('canvas');
            blankcanvas.width = dist.bfx.w;
            blankcanvas.height = dist.bfx.h;

        var ctx = blankcanvas.getContext('2d');

        var imageData = ctx.getImageData(0, 0, dist.bfx.w, dist.bfx.h);

        var data = imageData.data;

        dist.bfx.effect = dist.bfx.effectsrom[effs]

        dist.bfx.getDuration()

        dist.ComputeFrame( data , dist.bdata , dist.bfx.getType() , 0, dist.tickssy,dist.alpha, 0,
            dist.bfx.getAmplitude() ,dist.bfx.getAmplitudeAcceleration(),
            dist.bfx.getFrequency(), dist.bfx.getFrequencyAcceleration(),
            dist.bfx.getCompression(),dist.bfx.getCompressionAcceleration(),
            dist.bfx.getSpeed())


        ctx.putImageData(imageData, 0, 0);
        dist.fctx.drawImage(blankcanvas,0,0,dist.bfx.w,dist.bfx.h,0,0,416,416)
    }

}

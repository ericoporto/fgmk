function music(){

    var jsonGet = function(urlToGet) {
      var request = new XMLHttpRequest();
      request.open('get', urlToGet, false /*async*/);
      request.send();                   // bloqueia porque async esta false
      var json = request.responseText;  // string
      return JSON.parse(json);          // faz o parse da string e retorna objeto
    };

    var songList = (jsonGet("songlist.json"))["SongList"]

    var volume = 0.30

    var notes = {'C0':16.35 , 'C#0':17.32 , 'Db0':17.32 , 'D0':18.35 , 'D#0':19.45 , 'Eb0':19.45 ,
    'E0':20.60 , 'F0':21.83 , 'F#0':23.12 , 'Gb0':23.12 , 'G0':24.50 , 'G#0':25.96 , 'Ab0':25.96 ,
    'A0':27.50 , 'A#0':29.14 , 'Bb0':29.14 , 'B0':30.87 , 'C1':32.70 , 'C#1':34.65 , 'Db1':34.65 ,
    'D1':36.71 , 'D#1':38.89 , 'Eb1':38.89 , 'E1':41.20 , 'F1':43.65 , 'F#1':46.25 , 'Gb1':46.25 ,
    'G1':49.00 , 'G#1':51.91 , 'Ab1':51.91 , 'A1':55.00 , 'A#1':58.27 , 'Bb1':58.27 , 'B1':61.74 ,
    'C2':65.41 , 'C#2':69.30 , 'Db2':69.30 , 'D2':73.42 , 'D#2':77.78 , 'Eb2':77.78 , 'E2':82.41 ,
    'F2':87.31 , 'F#2':92.50 , 'Gb2':92.50 , 'G2':98.00 , 'G#2':103.83 , 'Ab2':103.83 , 'A2':110.00 ,
    'A#2':116.54 , 'Bb2':116.54 , 'B2':123.47 , 'C3':130.81 , 'C#3':138.59 , 'Db3':138.59 , 'D3':146.83 ,
    'D#3':155.56 , 'Eb3':155.56 , 'E3':164.81 , 'F3':174.61 , 'F#3':185.00 , 'Gb3':185.00 , 'G3':196.00 ,
    'G#3':207.65 , 'Ab3':207.65 , 'A3':220.00 , 'A#3':233.08 , 'Bb3':233.08 , 'B3':246.94 , 'C4':261.63 ,
    'C#4':277.18 , 'Db4':277.18 , 'D4':293.66 , 'D#4':311.13 , 'Eb4':311.13 , 'E4':329.63 , 'F4':349.23 ,
    'F#4':369.99 , 'Gb4':369.99 , 'G4':392.00 , 'G#4':415.30 , 'Ab4':415.30 , 'A4':440.00 , 'A#4':466.16 ,
    'Bb4':466.16 , 'B4':493.88 , 'C5':523.25 , 'C#5':554.37 , 'Db5':554.37 , 'D5':587.33 , 'D#5':622.25 ,
    'Eb5':622.25 , 'E5':659.26 , 'F5':698.46 , 'F#5':739.99 , 'Gb5':739.99 , 'G5':783.99 , 'G#5':830.61 ,
    'Ab5':830.61 , 'A5':880.00 , 'A#5':932.33 , 'Bb5':932.33 , 'B5':987.77 , 'C6':1046.50 , 'C#6':1108.73 ,
    'Db6':1108.73 , 'D6':1174.66 , 'D#6':1244.51 , 'Eb6':1244.51 , 'E6':1318.51 , 'F6':1396.91 , 'F#6':1479.98 ,
    'Gb6':1479.98 , 'G6':1567.98 , 'G#6':1661.22 , 'Ab6':1661.22 , 'A6':1760.00 , 'A#6':1864.66 , 'Bb6':1864.66 ,
    'B6':1975.53 , 'C7':2093.00 , 'C#7':2217.46 , 'Db7':2217.46 , 'D7':2349.32 , 'D#7':2489.02 , 'Eb7':2489.02 ,
    'E7':2637.02 , 'F7':2793.83 , 'F#7':2959.96 , 'Gb7':2959.96 , 'G7':3135.96 , 'G#7':3322.44 , 'Ab7':3322.44 ,
    'A7':3520.00 , 'A#7':3729.31 , 'Bb7':3729.31 , 'B7':3951.07 , 'C8':4186.01 , 'C#8':4434.92 , 'Db8':4434.92 ,
    'D8':4698.64 , 'D#8':4978.03 , 'Eb8':4978.03};

    var notesarr = []
    for (var key in notes) {
        notesarr.push([key,notes[key]]);
    }
    notesarr.sort(function(a,b) {return (a[1] > b[1]) ? 1 : ((b[1]> a[1]) ? -1 : 0);} );

    var audiocontext = new (window.AudioContext || window.webkitAudioContext)();


    function closestNoteFromFreq (freq,notearr) {
        var curr = notearr[0][1];
        var currnote = notearr[0][0];
        var diff = Math.abs (freq - curr);
        for (var val = 0; val < notearr.length; val++) {
            var newdiff = Math.abs (freq - notearr[val][1]);
            if (newdiff < diff) {
                diff = newdiff;
                curr = notearr[val][1];
                currnote = notearr[val][0];
            }
        }

        return currnote;
    }

    function hex2byte(n) {
        return parseInt(n,16)
    }

    function instrument(srcdata, ADSRenvelope,samplerate, audioCtx ,loop) {
        var audioCtx = audioCtx
        var datasz = srcdata.length
        var samplelength = datasz/4
        var attackTime = samplelength*ADSRenvelope[0]/(samplerate*1.0)
        var decayTime = samplelength*ADSRenvelope[1]/(samplerate*1.0)
        var sustainAmp = ADSRenvelope[2]*1.0
        var releaseTime = samplelength*ADSRenvelope[3]/(samplerate*1.0)
        var sample = new Float32Array(samplelength)


        var i = 0;
        var j = 0;
        while ( i + 4 < datasz ) {
            var sampsound = 0
            var temp = 0
            sampsound = (hex2byte(srcdata[i++])<<12)
            sampsound |= hex2byte(srcdata[i++])<<8
            sampsound |= hex2byte(srcdata[i++])<<4
            sampsound |= hex2byte(srcdata[i++])


            if(sampsound>32767) sampsound = sampsound-65536
            temp = (sampsound)/32768

            sample[j] = temp
            j++
        }

        var loop = (typeof loop === "undefined") ? [0,samplelength-1] : loop;

        var fftdata = new complex_array.ComplexArray(loop[1]-loop[0])

        var j = 0
        for(var k = loop[0]; k<loop[1]; k++){
            fftdata.real[j] = sample[k]
            fftdata.imag[j] = 0
            j++
        }

        //console.log(fftdata)

        fftdata.FFT()
        var maxv = 0
        var maxi = 0
        var temp = 0
        for(var i=0; i<samplelength; i++){
            temp = fftdata.real[i]*fftdata.real[i]+fftdata.imag[i]*fftdata.imag[i]
            if(maxv<temp) {
                maxv = temp
                maxi = i
            }
        }

        var fundamentalfreq = maxi*samplerate/(loop[1]-loop[0])
        var note = closestNoteFromFreq(fundamentalfreq, notesarr)

        var envelopeNode = audioCtx.createGain();
        var gainNode = audioCtx.createGain();

        gainNode.gain.value = volume

        envelopeNode.connect(gainNode)
        gainNode.connect(audioCtx.destination);

        this.play = function(notetoplay, volume, timetoplay){
            var timetoplay = (typeof timetoplay === "undefined") ? 0 : timetoplay;

            var source = audioCtx.createBufferSource();
            source.loop = false;

            var playbackRate = notes[notetoplay]/notes[note]

            var noteplaybackRate = Math.min(Math.round(samplerate*playbackRate), 170000)
            var noteplaybackRate = Math.max(noteplaybackRate, 8000)

            //console.log(noteplaybackRate)
            //console.log(samplelength)
            //console.log(note)

            var buffer = audioCtx.createBuffer(1, samplelength,noteplaybackRate);



            var data = buffer.getChannelData(0)
            for(var i=0; i<samplelength; i++){
                data[i]=sample[i]
            }

            source.buffer = buffer; // Assign our buffer to the source node buffer

            //sbuffer = buffer; // Assign our buffer to the source node buffer
            var now = audioCtx.currentTime;



            envelopeNode.gain.linearRampToValueAtTime(1, now + attackTime);
            envelopeNode.gain.linearRampToValueAtTime(sustainAmp, now + attackTime + decayTime);
            source.connect(envelopeNode);
            //console.log(timetoplay)

            source.start(timetoplay);

        }

    }


    this.makesong = function(songsarr, songdata, bpm){

        var masong = songdata["Patterns"]["1"]
        var offaudioctx = new OfflineAudioContext(2,44100*(masong[0].length+10)/(bpm/60),44100);

        var instruments = []

        instruments[0] = new instrument(ins_guitar, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx , [31458, 32481])
        instruments[1] = new instrument(ins_bass, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx)
        instruments[2] = new instrument(ins_kick, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx)
        instruments[3] = new instrument(ins_hatClosed, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx)
        instruments[4] = new instrument(ins_hatOpen, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx)
        instruments[5] = new instrument(ins_snare, [0.0, 0.6, 0.5, 0.7], 64000, offaudioctx)




        var now = offaudioctx.currentTime;
        now += 0.2

        //console.log(masong)

        var bps = bpm/60.0
        for(var i=0; i<masong[0].length ; i++){
            for(var k=0; k<masong.length ; k++){
                var chank = masong[k]
                if(i in chank){
                    if(chank[i].length){
                        //console.log(chank[i])
                        var _iinstrument = (1 in chank[i]) ? (chank[i][1]-1) : 1
                        var _ivolume = (2 in chank[i]) ? chank[i][2] : 0.5

                        instruments[_iinstrument].play(chank[i][0], _ivolume, now+ i/bps)
                    }
                }
            }
        }

        console.log("will try to render...")

        offaudioctx.startRendering().then(function(renderedBuffer) {
            console.log('rendered...');

            var buffer   = renderedBuffer;
            var UintWave = createWaveFileData(buffer);
            var base64   = btoa(uint8ToString(UintWave));

            songsarr.push(document.createElement('audio'))
            songsarr[songsarr.length-1].src = "data:audio/wav;base64," + base64;
            songsarr[songsarr.length-1].loop = true

            console.log('completed!');
        }, function(err) { console.log(err) }).catch(function(err) {
          console.log('Rendering failed: ' + err);
          // Note: The promise should reject when startRendering is called a second time on an OfflineAudioContext
      });

    }

    this.songs = []

    console.log(songList)

    for(var i=0; i<songList.length ; i++){
      this.makesong(this.songs, jsonGet(songList[i])["Song"], 500)
    }

    this.play = function () {
        this.songs[0].play()
    }

}

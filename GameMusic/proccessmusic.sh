#!/bin/bash
#filearr=("external/complex_array.js" "external/fft.js" "external/audiotob64.js" "instruments/bass.js" "instruments/guitar.js" "instruments/kick.js" "instruments/hatClosed.js" "instruments/hatOpen.js" "instruments/snare.js" "bgmusic.js")

# get length of an array
#arraylength=${#filearr[@]}

# use for loop read all values and indexes
#for (( i=1; i<${arraylength}+1; i++ )); do
   #do something to each element of array
#   echo "${filearr[$i]}"
#done

cat "external/complex_array.js" "external/fft.js" "external/audiotob64.js" "instruments/bass.js" "instruments/guitar.js" "instruments/kick.js" "instruments/hatClosed.js" "instruments/hatOpen.js" "instruments/snare.js" "bgmusic.js" > concat.js
node build.js

#!/bin/bash
#filearr=("helperf.js" "items.js" "menu.js" "engine.js" "actions.js" "screen.js" "hid.js" "printer.js" "title.js" "dist.js" "battle.js" "bootstrap.js")

# get length of an array
#arraylength=${#filearr[@]}

# use for loop read all values and indexes
#for (( i=1; i<${arraylength}+1; i++ )); do
   #do something to each element of array
#   echo "${filearr[$i]}"
#done

cat "rain.js" "helperf.js" "items.js" "menu.js" "feedback.js" "engine.js" "actions.js" "screen.js" "hid.js" "printer.js" "title.js" "dist.js" "battle.js" "bootstrap.js" > concat.js
node build.js

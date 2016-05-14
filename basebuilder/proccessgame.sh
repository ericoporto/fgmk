#!/bin/bash
fhere=`pwd`

buildfolder="$fhere/build"
mkdir -p "$buildfolder"

gamefolder="$fhere/../Game"


indexhtml="index.html"
minindexhtml="index.min.html"


read_dom () {
    local IFS=\>
    read -d \< ENTITY CONTENT
    local RET=$?
    FULLCONTENT="<$ENTITY> $CONTENT"
    TAG_NAME=${ENTITY%% *}
    ATTRIBUTES=${ENTITY#* }
    return $RET
}

parse_dom () {

    #if the is a javascript code, let's insert it.
    if [[ $TAG_NAME = "script" ]] ; then
        eval local $ATTRIBUTES
        echo "<script>"
        uglifyjs "$src"
        echo "</script>"
    elif [[ $TAG_NAME = "/script" ]] ; then
        echo ""

    #if there is a stylesheet, let's insert it.
    elif [[ $TAG_NAME = "link" ]] ; then
        eval local $ATTRIBUTES
        if [[ $rel = "stylesheet" ]] ; then
            echo "<style>"
            cat "$href"
            echo "</style>"

        else
            echo "$FULLCONTENT"
        fi
        

    elif [[ $TAG_NAME != "" ]] ; then
        echo "$FULLCONTENT"
    fi
}


cd "$gamefolder"

while read_dom; do
    parse_dom
done < "$indexhtml" > "$buildfolder/$minindexhtml"

cd "$buildfolder"

mv "$minindexhtml" "$indexhtml"

cp -r "$gamefolder/img" .
cp -r "$gamefolder/descriptors" .
cp -r "$gamefolder/audio" .
cp -r "$gamefolder/font" .
cp "$gamefolder/icon.png" .

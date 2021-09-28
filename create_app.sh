#!/bin/bash

# bottle_name app_name exe_path icon_path
#########################
BOTTLE=$1
APP=$2
EXE_PATH="$3"
ICON_PATH=$4
#########################
# create mac app
mkdir -p ./$APP.app/Contents/MacOS
mkdir -p ./$APP.app/Contents/Resources
cp Info.plist ./$APP.app/Contents
cp $ICON_PATH ./$APP.app/Contents/Resources
# app.ico

EXE_PATH=$(python3 reformat_name.py "$EXE_PATH")
echo $EXE_PATH

# create mac app entrypoint
touch ./$APP.app/Contents/MacOS/$APP.command
cat myscript.sh >> ./$APP.app/Contents/MacOS/main.command
sed -i .bak"s/<APP>/$APP/g" ./$APP.app/Contents/MacOS/main.command
sed -i .bak "s/<APP>/$APP/g" ./$APP.app/Contents/MacOS/main.command

# copy script app
cp script.sh ./$APP.app/Contents/Resources
sed -i .bak "s/<APP>/$APP/g" ./$APP.app/Contents/Resources/script.sh
sed -i .bak "s#<EXE_PATH>#$EXE_PATH#g" ./$APP.app/Contents/Resources/script.sh
sed -i .bak "s/<BOTTLE>/$BOTTLE/g" ./$APP.app/Contents/Resources/script.sh



chmod u+x ./$APP.app/Contents/MacOS/main.command
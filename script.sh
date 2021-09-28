#!/bin/bash

WINE_CREATE_BOTTLE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"

#########################
APP=<APP>
EXE_PATH="<EXE_PATH>"
BOTTLE=<BOTTLE>
#########################

if [ -f "$WINE" ]; then
    echo "wine found."
    sleep 1
else 
    echo "Plaese install brew and wine first. https://github.com/Gcenx/macOS_Wine_builds"
    echo "brew tap gcenx/wine"
    echo "brew install --cask --no-quarantine gcenx-wine-stable"
    exit 0
fi


echo "Launch $APP..."
$WINE --bottle $BOTTLE "$EXE_PATH"
echo "Shutdown..."
$WINE --bottle $BOTTLE wineboot --shutdown
osascript -e 'tell application "Terminal" to close first window'

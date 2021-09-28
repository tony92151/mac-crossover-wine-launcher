WINE_CREATE_BOTTLE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"

# /Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine --bottle Steam --wait-children --no-convert -- cxinstallfonts.exe 

WINE_TEM="win10_64"

echo "Create bottle: $1"
$WINE_CREATE_BOTTLE --bottle $1 --create --template $WINE_TEM --install

echo "\n"

echo "Bottle create at :/Users/$whoami/Library/Application Support/CrossOver/Bottles/$1"
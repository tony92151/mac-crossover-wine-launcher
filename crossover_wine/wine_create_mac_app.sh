WINE_CREATE_BOTTLE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"

WINE_TEM="win10_64"

echo "Open winecfg... bottle: $1"
$WINE --bottle $1 winecfg
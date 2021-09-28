WINE_CREATE_BOTTLE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"

WINE_TEM="win10_64"

echo "Install... bottle: $1"
# $WINE --bottle $1 --wait msiexec.exe $2

$WINE --bottle $1 --wait-children --no-convert --new-console msiexec.exe /i $2
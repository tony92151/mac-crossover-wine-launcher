WINE_CREATE_BOTTLE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle"
WINE="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"

WINE_TEM="win10_64"

create_bottle(){
  echo "Create bottle: $1"
  $WINE_CREATE_BOTTLE --bottle $1 --create --template $WINE_TEM --install
  echo ""
  echo "Bottle create at :/Users/$whoami/Library/Application Support/CrossOver/Bottles/$1"

}

ask_bottle(){
  read -p "Enter bottle name: "  bottle_name
}

#######################################################
#######################################################
echo "Welcome to mywine"

echo ''
#echo "(control+c to exit)"
select yn in "Create bottle" "Install" "Create macos app" "Remove bottle" "Exit"; do
    case $yn in
        "Create bottle" ) startype='cb'; break;;
        "Install" ) startype='install'; break;;
        "Create macos app" ) startype='cma'; break;;
        "Remove bottle") startype='rb'; break;;
        "Exit" ) exit 1; break;;
    esac
done

if [ $startype == "cb" ]
then
    ask_bottle
    create_bottle $bottle_name
elif [ $nodetype == "startype" ]
then

fi



#!/bin/bash

#########################
APP=<APP>
#########################

osascript -e "tell application \"Terminal\" to do script \"bash /Applications/$APP.app/Contents/Resources/script.sh \""


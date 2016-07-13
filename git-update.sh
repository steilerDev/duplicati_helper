#!/bin/bash

CURRENT_DIR=$(pwd)
GIT_DIR=$(dirname $(readlink -f $0))

echo "Not updated!"
echo "current dir: $CURRENT_DIR"
echo "git dir: $GIT_DIR"

cd $GIT_DIR

echo "Checking for duplicati_helper updates..."
git remote update > /dev/null
if [ $? -eq 0 ]; then
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})

    if [ $LOCAL != $REMOTE ]; then
        echo "Updating duplicati_helper and restarting command..."
        git pull
        cd $CURRENT_DIR
        exec $@
        echo "...done"
        exit
    else
        echo "...no update available"
    fi
else
    echo "...unable to get update"
fi

cd $CURRENT_DIR
echo "current dir: $(pwd)"

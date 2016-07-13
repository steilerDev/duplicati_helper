#!/bin/bash

CURRENT_DIR=$(pwd)
GIT_DIR=$(readlink -f $0)

echo "Not updated!"
echo "current dir: $CURRENT_DIR"
echo "git dir: $GIT_DIR"

cd $GIT_DIR

echo "Checking for duplicati_helper updates..."
git remote update > /dev/null

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ $LOCAL != $REMOTE ]; then
    echo "Updating duplicati_helper and restarting command..."
    git pull
    cd $CURRENT_DIR
    exec $@
    exit
else
    echo "...no update available"
    cd $CURRENT_DIR
fi

echo "current dir: $(pwd)"

#!/bin/bash

####
# This file will install mono, duplicati and the duplicati helpers
####

# Todo: Check and install: wget git gdb (for duplicati helper) 

DUPLICATI_PATH="/opt/duplicati/"
DUPLICATI_HELPER_PATH="/opt/duplicati_helper_temp/"

main () {
    echo "Welcome to the installer for mono, duplicati and the duplicati helpers!"

    check_root 
    #check_dependencies
  
    #yes_no "Do you want to install the latest mono version?" 1 "install_mono" 
    #yes_no "Do you want to install duplicati?" 1 "install_duplicati"
    #yes_no "Do you want to install duplicati helper scripts?" 1 "install_duplicati_helper"
    #yes_no "Do you want to configure your duplicati helper scripts?" 1 "config_duplicati_helper"
}

# This function checks if the current user has sudo rights
check_root () {
    echo "You need to be sudo to perform this installation"
    echo "Checking for root..."
    while true ; do
        sudo -v
        if [ "$?" = 0 ] ; then
            break
        fi
    done
    echo "...Passed"
    echo
}

check_dependencies () {
    echo "Updating apt-get..."
    sudo apt-get update > /dev/null
    echo "...Done"
    echo
    echo "Checking dependencies..."
    MISSING_DEP=""
    for dep in wget git gdb
    do
        if ! which $dep > /dev/null ; then
            echo "$dep not installed!"
            MISSING_DEP="$MISSING_DEP $dep"
        fi
    done
    if [ ! -z "$MISSING_DEP" ] ; then
        echo "Installing missing dependencies using apt-get..."
        sudo apt-get -y install $MISSING_DEP > /dev/null
        echo "...Done"
    else
        echo "All dependencies installed!"    
    fi
    echo
}

# This function installs the mono library, required to execute the application
install_mono () {
    echo -n "Adding mono to your apt sources..."
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
    echo "Done"
    echo

    echo "Installing mono with apt-get..."
    sudo apt-get install -y mono-complete > /dev/null
    echo "...Done"
    echo
}

# This function installs duplicati from source
install_duplicati () {
    DUPLICATI_TEMP="duplicati_latest.zip"

    get_path "Where do you want to install duplicati?" "DUPLICATI_PATH"
    cd $DUPLICATI_PATH
    echo
    
    echo -n "Getting URL for latest Duplicati release..."
    DUPLICATI_URL="$(curl -s https://api.github.com/repos/duplicati/duplicati/releases | grep browser_download_url | grep -P '(?<!-signatures).zip' | head -n 1 | cut -d '"' -f 4)"
    echo "Done"
    echo

    echo -n "Getting latest Duplicati release..."
    sudo wget $DUPLICATI_URL -O $DUPLICATI_TEMP > /dev/null 2>&1
    echo "Done"
    echo 

    echo -n "Installing latest Duplicati release..."
    sudo unzip $DUPLICATI_TEMP > /dev/null 2>&1
    rm -rf $DUPLICATI_TEMP
    echo "Done"
    echo
}

install_duplicati_helper () {
    get_path "Where do you want to install the duplicati helper scripts (NOTE: The files will be put into the 'duplicati_helper' subdirectory)" "DUPLICATI_HELPER_PATH"
    cd ${DUPLICATI_HELPER_PATH}
    echo

    echo -n "Getting latest Duplicati Helper release..."
    sudo git clone https://github.com/steilerDev/duplicati_helper.git > /dev/null 2>&1
    cd duplicati_helper
    DUPLICATI_HELPER_PATH=$(pwd)
    echo "Done" 
    echo

    if yes_no "Do you want to install the 'duplicati' script?" 1 ; then
        echo -n "Installing duplicati script..."
        sudo ln -s ${DUPLICATI_HELPER_PATH}/duplicati /bin/duplicati
        echo "Done"
    fi
    echo

    if yes_no "Do you want the shutdown delayed, in case a backup job is running?" 1 ; then
        echo -n "Installing shutdown script..."
        SHUTDOWN_BIN=$(which shutdown)
        sudo mv $SHUTDOWN_BIN ${SHUTDOWN_BIN}-bin
        sudo ln -s ${DUPLICATI_HELPER_PATH}/shutdown $SHUTDOWN_BIN
        sudo chown --reference=${SHUTDOWN_BIN}-bin ${DUPLICATI_HELPER_PATH}/shutdown
        sudo chmod --reference=${SHUTDOWN_BIN}-bin ${DUPLICATI_HELPER_PATH}/shutdown
        echo "Done"
    fi
    echo 

    if yes_no "Do you want to see the backup status upon login?" 1 ; then
        echo -n "Adding status script to '.bashrc'..."
        echo "## See the status of current and past duplicati backup jobs" >> $HOME/.bashrc
        echo "source ${DUPLICATI_HELPER_PATH}/duplicatirc" >> $HOME/.bashrc
        echo "Done"
    fi
    echo

    if yes_no "Do you want to enable <tab> auto completion for the duplicati helper script?" 1 ; then
        echo "Installing completion for duplicati..."
        if ! dpkg -s bash-completion > /dev/null 2>&1 ; then
            if yes_no "bash-completion is not installed on this system, do you want to install it?" 1; then
                echo "Installing bash-completion..."
                sudo apt-get install -y bash-completion > /dev/null
                echo "...Done"
                echo
            fi
        fi 

        if [ -d /etc/bash_completion.d/ ] ; then
           ln -s ${DUPLICATI_HELPER_PATH}/duplicati_completion /etc/bash_completion.d/duplicati_completion_temp
        else
            echo "!!!!!!!!"
            echo "Unable to link file, '/etc/bash_completion.d' does not exist"
            echo "!!!!!!!!"
        fi
        echo "Please make sure you have bash_completion activated in your '/etc/bash.bashrc' or '~/.bashrc' (you need the line '. /etc/bash_completion' in at least on of these files"
        echo "...Done"
    fi
    echo

    echo -n "Duplicating config files from templates..."
    cp ${DUPLICATI_HELPER_PATH}/duplicati.conf.example ${DUPLICATI_HELPER_PATH}/duplicati.conf
    cp ${DUPLICATI_HELPER_PATH}/backup.conf.example ${DUPLICATI_HELPER_PATH}/backup.conf
    echo "Done"

    echo -n "Fixing -eventually broken- references to config file..."
    for f in duplicati duplicatirc duplicati_completion shutdown; do
        sudo sed -i '/duplicati.conf/c\source '"${DUPLICATI_HELPER_PATH}"'/duplicati.conf' $f
    done
    echo "Done"
}

config_duplicati_helper () {
    echo "This functionality is not yet implemented"
}

# This function will ask the user to specify a path
# $1 The question string
# $2 The variable name, the path will be stored in
get_path () {
    read -p "$1: " -i "${!2}" -e path

    if [ ! -d "$path" ]; then
        echo "The path does not exist, creating it"
        sudo mkdir -p "$path" 
    fi
    printf -v $2 "$path"
}

# This function will prompt a yes no question. 
# $1 The question string
# $2 The default answer (0 for no, 1 for yes)
# $3 The callback function (no arguments, optional)
# The function returns 1 if no was selected and 0 if yes was selected ("if yes_no ... ; then" results in true if true was selected)
yes_no () {
    if [ "$2" = 1 ] ; then
        QUESTION="$1 [(y)|n]: "
    else
        QUESTION="$1 [y|(n)]: "
    fi

    while true ; do
        read -p "$QUESTION" yn
        case $yn in
            [Yy]* ) 
                $3
                return 0 ;;
            [Nn]* ) 
                return 1 ;;
            "" ) 
                if [ "$2" = 1 ] ; then
                    $3
                    return 0
                else
                    return 1
                fi ;;
            * ) 
                echo "Please answer yes or no.";;
        esac
    done
    return 0;
}

test () {
    echo "Works"
}

main $@
exit -1

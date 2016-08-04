#!/bin/bash

####
# This file will install mono, duplicati and the duplicati helpers
####

DUPLICATI_PATH="/opt/duplicati/"
DUPLICATI_HELPER_PATH="/opt/"

SHUTDOWN_BIN=""

main () {
    echo
    echo "#######################################################################"
    echo "Welcome to the installer for mono, duplicati and the duplicati helpers!"
    echo "#######################################################################"
    echo "Made with <3 by steilerDev"
    echo

    check_root 
    check_dependencies
  
    yes_no "Do you want to install the latest mono version?" 1 "install_mono" 
    yes_no "Do you want to install duplicati?" 1 "install_duplicati"
    yes_no "Do you want to install duplicati helper scripts?" 1 "install_duplicati_helper"
    yes_no "Do you want to configure your duplicati helper scripts?" 1 "config_duplicati_helper"
    
    echo "All finished, enjoy!"
    echo
    echo "Made by steilerDev (https://github.com/steilerDev/)"
    echo "For support and information go to https://github.com/steilerdev/duplicati_helper/"
    echo "Licensed under a GNU General Public License, Version 3"
    exit 0
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
    for dep in wget git gdb curl unzip
    do
        if ! which $dep > /dev/null ; then
            echo "$dep not installed!"
            MISSING_DEP+="$dep "
        fi
    done
    if [ ! -z "$MISSING_DEP" ] ; then
        yes_no "Do you want to install the missing dependiencies ($MISSING_DEP). Not installing these dependiencies might result in unexpected behaviour of the appliction." 1 "install_dependencies" 
    fi
    echo    
}

install_dependencies () {
    if [ ! -z "$MISSING_DEP" ] ; then
        echo "Installing missing dependencies using apt-get (This might take a while)..."
        sudo apt-get -y install $MISSING_DEP > /dev/null
        echo "...Done"
    else
        echo "...All dependencies installed!"    
    fi
}

# This function installs the mono library, required to execute the application
install_mono () {
    echo -n "Adding mono to your apt sources..."
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF > /dev/null 2> /dev/null
    sudo sh -c "echo \"deb http://download.mono-project.com/repo/debian wheezy main\" >> /etc/apt/sources.list.d/mono-xamarin.list"
    echo "Done"
    echo

    echo "Installing mono with apt-get (This might take a while)..."
    sudo apt-get install -y mono-complete > /dev/null
    sudo apt-get update > /dev/null
    sudo apt-get install -y mono-devel mono-complete > /dev/null
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

    echo -n "Getting latest Duplicati release (This might take a while)..."
    sudo wget $DUPLICATI_URL -O $DUPLICATI_TEMP > /dev/null 2>&1
    echo "Done"
    echo 

    echo -n "Installing latest Duplicati release..."
    sudo unzip $DUPLICATI_TEMP > /dev/null 2>&1
    sudo rm -f $DUPLICATI_TEMP
    echo "Done"
    echo
}

install_duplicati_helper () {
    get_path "Where do you want to install the duplicati helper scripts (NOTE: The files will be put into the 'duplicati_helper' subdirectory)" "DUPLICATI_HELPER_PATH"
    cd ${DUPLICATI_HELPER_PATH}
    echo

    echo "Getting latest Duplicati Helper release..."
    sudo git clone https://github.com/steilerDev/duplicati_helper.git > /dev/null
    cd duplicati_helper
    DUPLICATI_HELPER_PATH=$(pwd)
    echo "...Done" 
    echo
    
    echo -n "Duplicating config files from templates..."
    sudo cp ${DUPLICATI_HELPER_PATH}/duplicati.conf.example ${DUPLICATI_HELPER_PATH}/duplicati.conf
    sudo cp ${DUPLICATI_HELPER_PATH}/backup.conf.example ${DUPLICATI_HELPER_PATH}/backup.conf
    echo "Done"

    if yes_no "Do you want to install the 'duplicati' script?" 1 ; then
        echo -n "Installing duplicati script..."
        sudo ln -s ${DUPLICATI_HELPER_PATH}/duplicati /bin/duplicati
        echo "Done"
    fi
    echo

    if yes_no "Do you want the shutdown delayed, in case a backup job is running?" 1 ; then
        echo -n "Installing shutdown script..."
        SHUTDOWN_BIN=$(sudo which shutdown)
        if [ -z "$SHUTDOWN_BIN" ] ; then
            echo "Unable to find shutdown binary, unable to install shutdown delay!"
        else
            sudo mv "$SHUTDOWN_BIN" "${SHUTDOWN_BIN}-bin"
            sudo ln -s ${DUPLICATI_HELPER_PATH}/shutdown $SHUTDOWN_BIN
            set_config_value "FP_SHUTDOWN" "$(stat -c "%a" ${SHUTDOWN_BIN}-bin)" "The file permissions, retrieved from the original shutdown binary (${SHUTDOWN_BIN}-bin)"
            sudo chown --reference=${SHUTDOWN_BIN}-bin ${DUPLICATI_HELPER_PATH}/shutdown
            sudo chmod --reference=${SHUTDOWN_BIN}-bin ${DUPLICATI_HELPER_PATH}/shutdown
            SHUTDOWN_BIN=${SHUTDOWN_BIN}-bin
            echo "Done"
        fi
    fi
    echo 

    if yes_no "Do you want to see the backup status upon login?" 1 ; then
        echo -n "Adding status script to '.bashrc'..."
        sudo sh -c "echo \"source ${DUPLICATI_HELPER_PATH}/duplicatirc\" >> $HOME/.bashrc"
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
           sudo ln -s ${DUPLICATI_HELPER_PATH}/duplicati_completion /etc/bash_completion.d/duplicati_completion
        else
            echo "!!!!!!!!"
            echo "Unable to link file, '/etc/bash_completion.d' does not exist"
            echo "!!!!!!!!"
        fi
        echo "    Please make sure you have bash_completion activated in your '/etc/bash.bashrc' or '~/.bashrc' (you need the line '. /etc/bash_completion' in at least on of these files"
        echo "...Done"
    fi
    echo


    echo -n "Fixing -eventually broken- references to config file..."
    for f in duplicati duplicatirc duplicati_completion shutdown; do
        sudo sed -i '0,/duplicati.conf/c\source '"${DUPLICATI_HELPER_PATH}"'/duplicati.conf' $f
    done
    echo "Done"
}

config_duplicati_helper () {
    echo "The following steps will configure your duplicati helper, if you don't provide a value, the default value will be used"
    echo

    print_config_header "Connection settings"
    config_duplicati_helper_item "BASE_URL" "amzcd:///" "Specify the URL for your backups. Each backup will be put into a subfolder of this directory with its respective name." "NOTE: The helper was only tested with Amazon Cloud Drive, feel free to report problems with other providers using https://github.com/steilerdev/duplicati_helper/issues."
    config_duplicati_helper_item "AUTH_ID" "" "Specify the authid for your provider" "The token can be obtained from https://duplicati-oauth-handler.appspot.com"

    print_config_header "Log settings"
    config_duplicati_helper_item "LOG_PATH" "/var/log/" "Specify the directory, where the log files should be written to"
    config_duplicati_helper_item "LOG_LEVEL" "Warning" "Specify the log level of duplicati" "Available log levels: \"Error\", \"Warning\", \"Information\", \"Profiling\""

    print_config_header "Server settings"
    config_duplicati_helper_item "SERVER_PORT" "8200" "Specify the port, the webinterface should be accessible from"
    config_duplicati_helper_item "SERVER_PAS" "Password1!" "Specify the password for the webinterface"

    print_config_header "Helper settings"
    config_duplicati_helper_item "HELPER_AUTO_UPDATE" "true" "Do you want to enable auto-updates for the helper programs before executing the 'duplicati' command?" "Choose 'true' or 'false', manual updates are still possible through 'duplicati update'"
    config_duplicati_helper_item "DUPLICATI_UPDATE_POLICY" "InstallBefore" "Specify the update strategy of duplicati itself" "Available values are: 'CheckBefore', 'CheckDuring', 'CheckAfter', 'InstallBefore', 'InstallDuring', 'InstallAfter', 'Never'"

    print_config_header "Helper file permissions"
    config_duplicati_helper_item "MANAGE_FILE_PERMISSIONS" "true" "Do you want duplicati to set the file permissions, in order to keep your files as safe as possible?" "This should be done, since updating the helper might result in changed file permissions. The next configuration items will ask for your prefered user and access rights."
    config_duplicati_helper_item "DUPLICATI_USER" "root" "The user, that will be able to execute duplicati (technically this will be the owner of the folder and all files within" "This user should be root, in order to protect your files against unintended access from other users on the system, as well as ensure full access rights and permissions (e.g. creating snapshot) during backup creation"
    config_duplicati_helper_item "DUPLICATI_GROUP" "root" "The group, that will be able to execute duplicati (technically this will be the owner group of the folder and all files within" "This group should be root, in order to protect your files against unintended access from other users on the system, as well as ensure full access rights and permissions (e.g. creating snapshot) during backup creation"
    config_duplicati_helper_item "FP_BACKUP_CONF" "600" "Please set the access rights to 'backup.conf'" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    config_duplicati_helper_item "FP_DUPLICATI" "744" "Please set the access rights to the 'duplicati' script" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    config_duplicati_helper_item "FP_DUPLICATI_CONF" "644" "Please set the access rights to 'duplicati.conf'" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    config_duplicati_helper_item "FP_DUPLICATI_COMPLETION" "755" "Please set the access rights to 'duplicati_completion'" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    config_duplicati_helper_item "FP_DUPLICATIRC" "755" "Please set the access rights to 'duplicatirc'" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    config_duplicati_helper_item "FP_INSTALL" "644" "Please set the access rights to 'install.sh'" "The value needs to be given as octal. It is highly recommended to use the proposed mode, in order to ensure high privacy and full functionality"
    set_config_value "FP_BACKUP_STATUS" "644" "The file permissions for the backup status file. This file should be readable by every user and will be created later"

    echo -n "Finishing configuration..."
    # Auto configuration of some values, that might change due to installation is done now.
    set_config_value "DUPLICATI" "mono ${DUPLICATI_PATH}/Duplicati.CommandLine.exe" "This is the path to the duplicati executable"
    set_config_value "DUPLICATI_SERVER" "mono ${DUPLICATI_PATH}/Duplicati.Server.exe" "This is the path to the duplicati server executable"
    set_config_value "BACKUP_CONFIG" "${DUPLICATI_HELPER_PATH}/backup.conf" "This is the path to the backup configuration file"
    set_config_value "DUPLICATIRC" "${DUPLICATI_HELPER_PATH}/duplicatirc" "This is the path to the duplicatirc file"
    set_config_value "BACKUP_STATUS_FILE" "${DUPLICATI_HELPER_PATH}/backup.status" " This status file will hold the information about the status of previous backups. Use duplicatirc to display it at log in."
    set_config_value "SHUTDOWN_BIN" "$SHUTDOWN_BIN" "The path to the original shutdown binary"
    
    # Now making sure that all the advanced default variables will be there
    set_config_value "LOG_PREFIX" "duplicati" "This is the prefix every log file will get. The log files will be named using the following schema: prefix.backupName.log"
    set_config_value "COMPRESSION_MODULE" '--compression-module=\"7z\" --7z-compression-level=\"7\"' "These are command line arguments for duplicati, sorted by topic"
    set_config_value "ENCRYPTION_MODULE" '--encryption-module=\"aes\"' "These are command line arguments for duplicati, sorted by topic"
    set_config_value "BACKUP_MODULE" '--number-of-retries=\"25\" --keep-time=\"3M\" --dblock-size=\"200mb\" --snapshot-policy=\"on\"' "These are command line arguments for duplicati, sorted by topic"
    set_config_value "PID_DIR" "/run/" "The directory to store the PID files of running duplicati jobs"
    set_config_value "DUPLICATI_PID_PREFIX" "duplicati" "The prefix every duplicati job PID file will get. The following schema will be used: prefix.backupName.pid"
    set_config_value "SHUTDOWN_PID_PREFIX" "shutdown" "The name of the shutdown postponing script's PID" "NOTE: This should not be the same, or start the same as DUPLICATI_PID_PREFIX, otherwise the shutdown script will wait on itself"
    
    # Setting permissions, according to config (only if user agreed on managing file permissions by duplicati
    set_permissions

    echo "Done" 
    echo
    echo "Now the configuration is done, configure your backup by editing the file ${DUPLICATI_HELPER_PATH}/backup.conf"
    echo
}

set_permissions () {
    if [ $MANAGE_FILE_PERMISSIONS = "true" ] ; then
        echo -n "Setting permissions..."

        sudo chown -R ${DUPLICATI_USER}:${DUPLICATI_GROUP} ${DUPLICATI_HELPER_PATH}
        sudo chmod $FP_BACKUP_CONF ${DUPLICATI_HELPER_PATH}/backup.conf
        sudo chmod $FP_DUPLICATI ${DUPLICATI_HELPER_PATH}/duplicati
        sudo chmod $FP_DUPLICATI_CONF ${DUPLICATI_HELPER_PATH}/duplicati.conf
        sudo chmod $FP_DUPLICATI_COMPLETION ${DUPLICATI_HELPER_PATH}/duplicati_completion
        sudo chmod $FP_DUPLICATIRC ${DUPLICATI_HELPER_PATH}/duplicatirc
        sudo chmod $FP_INSTALL ${DUPLICATI_HELPER_PATH}/install.sh
        sudo chmod $FP_SHUTDOWN ${DUPLICATI_HELPER_PATH}/shutdown
        echo "Done"
    fi
}

# Prints a header, shown during configuration
# $1 Label of header, max lenghts: 25 chars
print_config_header () {
    echo "############################"
    echo -n "# "
    echo -n "$1                           " | head -c 25
    echo " #"
    echo "############################"

}

# This function will configure a single item in the configuration file. The file needs to be located in $DUPLICATI_HELPER_PATH/duplicati.conf 
# $1 Item name (key in config file)
# $2 Default value
# $3 Statements, displayed to the user 
# $4 Second statement, displayed to the user (optional)
config_duplicati_helper_item () {

    echo "$3"
    if [ ! -z "$4" ] ; then
        echo "$4"
    fi

    read -p "[$2]: " -e answer
    if [ -z "$answer" ] ; then
        answer=$2
    fi
    set_config_value "$1" "$answer" "$3" "$4"
    echo
}

# This function sets a config value in the config file $DUPLICATI_HELPER_PATH/duplicati.conf
# $1 The key
# $2 The value
# $3 Comment for the key-value pair, in case entry did not exist yet (optional)
# $4 Comment for the key-value pair, in case entry did not exist yet (optional)
set_config_value () {
    CONFIGFILE="${DUPLICATI_HELPER_PATH}/duplicati.conf"
    if [ ! -e "$CONFIGFILE" ] ; then
        sudo touch $CONFIGFILE
    fi
    
    if grep -q $1 $CONFIGFILE ; then
        sudo sed -i '/'"$1"'/c\'"$1"'="'"$2"'"' $CONFIGFILE
    else
        if [ ! -z "$3" ] ; then
            sudo sh -c "echo \"# $3\" >> $CONFIGFILE"
        fi
        if [ ! -z "$4" ] ; then
            sudo sh -c "echo \"# $4\" >> $CONFIGFILE"
        fi
        sudo sh -c "echo \"$1=\\\"$2\\\"\" >> $CONFIGFILE"
    fi
    
    # Setting value, in order to make it avaiable in this script
    eval "$1=\"$2\""
}

# This function will ask the user to specify a path
# The function will return an existing path without trailing slashes!
# $1 The question string
# $2 The variable name, the path will be stored in
get_path () {
    read -p "$1: " -i "${!2}" -e path

    if [ ! -d "$path" ]; then
        echo "The path does not exist, creating it"
        sudo mkdir -p "$path" 
    fi
    path=${path%/}
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

main $@
exit -1

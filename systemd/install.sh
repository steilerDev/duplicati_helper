#! /bin/bash
source /opt/duplicati_helper/duplicati.conf

echo "Installing systemd service & timer, run as root!"
ln -s /opt/duplicati_helper/systemd/duplicati@.service /etc/systemd/system/
ln -s /opt/duplicati_helper/systemd/duplicati-daily3am@.timer /etc/systemd/system/
ln -s /opt/duplicati_helper/systemd/duplicati-every3d@.timer /etc/systemd/system/
ln -s /opt/duplicati_helper/systemd/duplicati-every7d@.timer /etc/systemd/system/
systemctl daemon-reload

setInterval () {
    echo "#####################################"
    echo "# Configuration: $1"
    echo "#####################################"
    PS3="Please select interval for '${1}': "
    options=("Daily at 3am" "Every 3 days" "Every 7 days" "Never")
    select opt in "${options[@]}" ; do
        case $opt in
            "Daily at 3am")
                echo "Installing timer for '$1' config: Daily at 3am..."
                ln -s /opt/duplicati_helper/systemd/duplicati-daily3am@.timer /etc/systemd/system/multi-user.target.wants/duplicati-daily3am@${1}.timer
                systemctl daemon-reload
                systemctl start duplicati-daily3am@${1}.timer 
                break
                ;;
            "Every 3 days")
                echo "Installing timer for '$1' config: Every 3 days..."
                ln -s /opt/duplicati_helper/systemd/duplicati-every3d@.timer /etc/systemd/system/multi-user.target.wants/duplicati-every3d@${1}.timer
                systemctl daemon-reload
                systemctl start duplicati-every3d@${1}.timer 
                break
                ;;
            "Every 7 days")
                echo "Installing timer for '$1' config: Every 7 days..."
                ln -s /opt/duplicati_helper/systemd/duplicati-every7d@.timer /etc/systemd/system/multi-user.target.wants/duplicati-every7d@${1}.timer
                systemctl daemon-reload
                systemctl start duplicati-every7d@${1}.timer 
                break
                ;;
            "Never")
                echo "Not installing timer for '$1' config."
                break
                ;;
            *)
                echo "Invalid option!" ;;
        esac
    done

}

# Iterate over all configured backups
BACKUPS=""
while read -r name path pas LOCAL_OPTIONS ; do
    if [[ $name == \#* ]] ; then
        # Ignore lines with pound
        continue
    else
        BACKUPS="$BACKUPS $name"
    fi
done < "${BACKUP_CONFIG}"

for BACKUP in $BACKUPS ; do
    setInterval $BACKUP
done

systemctl daemon-reload

echo
echo "#####################################"
echo "# Please check all installed timers #"
echo "#####################################"
systemctl list-timers


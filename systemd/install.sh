#! /bin/bash
echo "Installing systemd service & timer, run as root!"
ln -s /opt/duplicati_helper/systemd/duplicati.service /etc/systemd/system/
ln -s /opt/duplicati_helper/systemd/duplicati.timer /etc/systemd/system/
ln -s /opt/duplicati_helper/systemd/duplicati.timer /etc/systemd/system/multi-user.target.wants/

systemctl daemon-reload
systemctl start duplicati.timer
systemctl list-timers


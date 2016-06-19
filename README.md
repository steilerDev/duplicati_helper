# Duplicati_Helper
This repository is a collection of helper scripts, simplifying the interface of duplicati, making it reusable, easy to configure and ready for cron deployment. This collection of scripts is intended for administrators, solely relying on the command line interface on Linux machines.

**Disclaimer**: This project is developed independent from [duplicati](https://github.com/duplicati/duplicati) and is intended to be used with duplicati v.2 Beta. I am only testing these helpers with Amazon Cloud Drive, other providers should work as well, however you might need to modify the script slightly.

# Components
This repository contains different components, that can be used indipendent of each other. However I recommend to use all of them, in order to get the full experience.

## duplicati

### duplicati.conf

### backup.conf

## duplicatirc

## shutdown

# Installation
1. Clone the repository (suggested location: `/opt/duplicati_helper/`)
2. Link binary: `ln -s /opt/duplicati_helper/duplicati /bin/duplicati`
3. In case you want a shutdown delayed by running duplicati jobs, do the following:
  * `mv /sbin/shutdown /sbin/shutdown-bin`
  * `ln -s /opt/duplicati_helper/shutdown`
  * Make sure the access rights to `/opt/duplicati_helper/shutdown` match `/sbin/shutdown-bin`
4. In order to show the backup status during log-in on the console, include `source /opt/duplicati_helper/duplicatirc` in your `~/.bashrc` (or similiar depending on your bash)
5. Configure your general duplicati settings based on the provided example in `/opt/duplicati_helper/duplicati.conf.example`
6. Configure your backups based on the provided example in `/opt/duplicati_helper/backup.conf.example`
7. In order for the helper scripts to use your `duplicati.conf` file, you either need to move it to `/opt/duplicati_helper/duplicati.conf`, or you need to modify the second line (`source /opt/duplicati_helper/duplicati.conf`) of `duplicatirc`, `duplicati` and `shutdown`, pointing to your configuration path.

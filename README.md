# Duplicati Helper
This repository is a collection of helper scripts, simplifying the interface of duplicati, making it reusable, easy to configure and ready for cron deployment. This collection of scripts is intended for administrators, solely relying on the command line interface on Linux machines.

**Disclaimer**: This project is developed independent from [duplicati](https://github.com/duplicati/duplicati) and is intended to be used with duplicati v.2 Beta. I am only testing these helpers with Amazon Cloud Drive, other providers should work as well, however you might need to modify the script slightly.

# Components
This repository contains different components, that can be used indipendent of each other. However I recommend to use all of them, in order to get the full experience.

## duplicati
This script is simplifying the interface to duplicati, by introducing a configuartion file based execution of the backups. An up-to-date information about the functionality and the currently configured backups within your instance can be found by executing `duplicati help`. The following table will show the current functionalities:

Command | Functionality 
--- | --- 
`duplicati help` | Shows a full list of available commands and configured backups.
`duplicati {backup | repair} <backup_config_name>` | Starts the backup/repair of a pre-configured backup job. The backup will be put into a subfolder on your cloud provider with the configured backup name, the log will be written to the configured log directory with the name `duplicati.<backup_config_name>.log`. The backup is defined within `backup.conf` (see below). Optionally the backup name can be followed by the argument `quiet`, relaying all output to the log file (functionality not fully working, since [duplicati has a bug there](https://github.com/duplicati/duplicati/issues/1752). 
`duplicati kill <backup_config_name>` | Kills a running backup job with the supplied name
`duplicati server` | Starts the duplicati webserver, with the supplied configuration from `duplicati.conf` (see below).
`duplicati usage` | Shows the usage of currently running backup jobs using `top`.
`duplicati status` | Shows the output of the `duplicatirc` file (see below).
`duplicati command <duplicati arguments>` | Invokes the duplicati CLI with the provided arguments.

### duplicati.conf
This file contains the basic configuration of duplicati. The default path is `/opt/duplicati_helper/duplicati.conf`. In case you want to change the location of this file, you need to modify `duplicati`, `duplicatirc` and `shutdown`, as described in the intallation instructions below (bullet point 7). An example configuration with all required properties is provided within this repository (`duplicati.conf.example`).

### backup.conf
This file contains the configuration of your backup jobs. It contains the backup's password. The password or name are not allowed to contain white spaces. Make sure you restrict the access rights to the user who is executing the backups. In case you want to change the location of the file (default: `/op/duplicati_helper/backup.conf`) you need to modify `duplicati.conf`'s `BACKUP_CONFIG` value. An example configuration is provided within this repository (`backup.conf.example`).  

## duplicatirc
This script is intended to give a summary of every backup job's current status upon log in. A "+" within the first column indicates, that this entry was added or updated since your last log in. The status of backups is tracked within a status file. The location of this file is specified within `duplicati.conf`'s `BACKUP_STATUS_FILE` variable.

## shutdown
This script is a drop-in replacement for the shutdown procedure, checking if there are any running duplicati jobs and postponing the shutdown until all jobs finished. Upon calling `shutdown` it will notify all open terminals, that a shutdown is scheduled, but delayed. A scheduled shutdown can be canceled using `shutdown -c`. In case a shutdown is scheduled, `duplicatirc` will display that information.

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

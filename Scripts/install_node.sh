#!/bin/bash

echo 'password' | sudo -S apt-get update -y

echo 'password' | sudo -S apt upgrade -y

echo 'password' | sudo -S apt-get install lm-sensors -y

echo 'password' | sudo -S apt-get install wireless-tools -y

echo 'password' | sudo -S apt-get install hostapd -y

echo 'password' | sudo -S apt-get install wpasupplicant -y

echo 'password' | sudo -S apt-get install dnsmasq -y

echo 'password' | sudo -S apt-get install unzip -y

## Check if you have python3 installed, python3 --version
## Uncomment the next line if you don't
##echo 'password' | sudo -S apt-get install python3 -y

## dont_delete is the folder with all the
## Files needed in order to run the software in the boot

echo 'password' | sudo -S mkdir /home/amazing/dont_delete

mkdir /home/amazing/it_user

echo 'password' | sudo -S mv /home/amazing/files.zip /home/amazing/dont_delete/


## files.zip was sent to the node via scp (secure copy)
## Has APIPEI.py, init_node.sh, requirementsAPI.txt, node_init.py


echo 'password' | sudo -S unzip /home/amazing/dont_delete/files.zip -d /home/amazing/dont_delete/

echo 'password' | sudo -S rm -r /home/amazing/dont_delete/files.zip

echo 'password' | sudo -S mv /home/amazing/dont_delete/files/* /home/amazing/dont_delete/

echo 'password' | sudo -S rm -r /home/amazing/dont_delete/files/

echo 'password' | sudo -S chown root /home/amazing/dont_delete/init_node.sh

echo 'password' | sudo -S chmod 775 /home/amazing/dont_delete/init_node.sh

echo 'password' | sudo -S apt-get install python3-pip -y

echo 'password' | sudo -S pip3 install virtualenv

echo 'password' | sudo -S virtualenv /home/amazing/dont_delete/venv

source /home/amazing/dont_delete/venv/bin/activate

echo 'password' | sudo -S pip3 install -r /home/amazing/dont_delete/requirementsAPI.txt

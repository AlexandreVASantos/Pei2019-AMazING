#!/bin/bash

echo 'amazing' | sudo -S apt-get update -y

echo 'amazing' | sudo -S apt upgrade -y

echo 'amazing' | sudo -S apt-get install lm-sensors -y

echo 'amazing' | sudo -S apt-get install wireless-tools -y

echo 'amazing' | sudo -S apt-get install wpasupplicant -y

echo 'amazing' | sudo -S mkdir /home/amazing/dont_delete

echo 'amazing' | sudo -S cp /media/cdrom/* /home/amazing/dont_delete/

echo 'amazing' | sudo -S chown root /home/amazing/dont_delete/init_node.sh

echo 'amazing' | sudo -S chmod 775 /home/amazing/dont_delete/init_node.sh

echo 'amazing' | sudo -S chown root /home/amazing/dont_delete/wake_up.sh

echo 'amazing' | sudo -S chmod 775 /home/amazing/dont_delete/wake_up.sh

echo 'amazing' | sudo -S apt-get install python3-pip -y

echo 'amazing' | sudo -S pip3 install virtualenv

echo 'amazing' | sudo -S virtualenv /home/amazing/dont_delete/venv

source /home/amazing/dont_delete/venv/bin/activate

echo 'amazing' | sudo -S pip3 install -r /home/amazing/dont_delete/requirements.txt


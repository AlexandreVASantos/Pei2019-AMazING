#!/bin/bash


echo 'amazing' | sudo -S mkdir /home/amazing/dont_delete

echo 'amazing' | sudo -S cp /media/cdrom/* /home/amazing/dont_delete/

echo 'amazing' | sudo -S chown root /home/amazing/dont_delete/init_node.sh

echo 'amazing' | sudo -S chmod 775 /home/amazing/dont_delete/init_node.sh

echo 'amazing' | sudo -S apt-get install python-pip -y

echo 'amazing' | sudo -S pip install virtualenv

virtualenv /home/amazing/dont_delete/env

source /home/amazing/dont_delete/env/bin/activate

echo 'amazing' | sudo -S pip install -r /home/amazing/dont_delete/requirements.txt


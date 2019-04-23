#!/bin/bash


#sudo chown root path/to/script.sh 
#sudo chmod 775 path/to/script.sh
#sudo crontab -e
#@reboot /path/to/script.sh
source /home/alexandre/Desktop/SwitchController/venv/bin/activate

python /home/alexandre/Desktop/APIPEI.py

python3 /home/alexandre/Desktop/node_up.py
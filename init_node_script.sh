#!/bin/bash

#sudo chown root /path/to/script.sh
#sudo chmod 776 /path/to/script.sh
#sudo crontab -e
#@reboot /path/to/script.sh


source /home/amazing/dont_delete/venv/bin/activate

python3 /home/amazing/dont_delete/APIPEI.py &

#python3 /home/amazing/dont_delete/node_init.py &

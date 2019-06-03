#!/bin/bash


echo 'amazing' | sudo -S bash /home/amazing/dont_delete/wake_up.sh


source /home/amazing/dont_delete/venv/bin/activate

sudo python3 /home/amazing/dont_delete/APIPEI.py &

sudo python3 /home/amazing/dont_delete/node_init.py &

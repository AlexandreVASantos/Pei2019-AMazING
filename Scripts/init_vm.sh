#!/bin/bash


source /home/ubuntu/apps/venv/bin/activate

/home/ubuntu/apps/kafka_2.12-2.2.1/bin/zookeeper-server-start.sh /home/ubuntu/apps/kafka_2.12-2.2.1/config/zookeeper.properties &

sleep 10

/home/ubuntu/apps/kafka_2.12-2.2.1/bin/kafka-server-start.sh /home/ubuntu/apps/kafka_2.12-2.2.1/config/server-1.properties &

sleep 10

/home/ubuntu/apps/kafka_2.12-2.2.1/bin/kafka-server-start.sh /home/ubuntu/apps/kafka_2.12-2.2.1/config/server-2.properties &

sleep 10

sudo python3 /home/ubuntu/apps/SwitchController/SwitchController/manage.py runserver 192.168.85.228:8000 &

sleep 5

sudo python3 /home/ubuntu/apps/NodeConfigApp/AMazING/manage.py runserver 192.168.85.228:16000 &

sleep 5

sudo python3 /home/ubuntu/apps/SwitchController/SwitchController/manage.py process_tasks &

sleep 5

sudo python3 /home/ubuntu/apps/NodeConfigApp/AMazING/manage.py process_tasks &


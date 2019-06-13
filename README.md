# Pei -  AMazING

## Nodes

### Overview
For the nodes we used an APU board from PCEngines.

### Preparing OS
To Operating System we chose Ubuntu Server 18.04 LTS, which is available here. In case you choose the APU Board from PCEngines pick the 64-bit PC (AMD64) server install image, because with the others there is no compability and you have to do incrementals updates from Ubuntu Server 14.04 LTS.

After the OS installation is completed you need to install the packages needed by our software to run the Restful API and connect nodes to kafka in order to manage if their running fine. If you desire to have separated virtual environment, please change the following script to your needs. The script for one virtual environment with all software needed is install_node.sh.


The package kafka-python in requirementsAPI.txt is needed for the interaction between nodes and Switch Controller App. Remove it if not needed.
						


Next you need to put the scripts running at boot, use systemd or create a crontab as root:


$ sudo crontab -e
						


Choose option 1 and at the end of the file write:


@reboot path/to/script/name_of_script.sh
						


Now just need to CTRL+X and then ENTER. At this moment everything you need is installed in the node and running at boot time. If you reboot, you can check if it is running fine with $ ps -aux or $ curl localhost:5000

## Restful API

### Overview
The node restful API, running on nodes and being the bridge between the nodes and the Node Config App, we decided to go with Python with a little help of Flask. We even went further and used a microframework, Flask-Restful. Flask is a powerfull framework that in opposition with Django it is better user firendly when no web page is needed.

If you have done the previous step correctly you are now able to run a Flask API.

## Node Config App

### Overview
Our Node Config App provides an abstraction layer for the end user when performing wireless configurations. We chose Python for building our app backend in addition with Django framework. For the front end html, css and javascript was used.

### Preparing environment

$ sudo apt-get update
$ sudo apt-get install python3-pip
$ sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
$ sudo pip3 install virtualenv
$ sudo virtualenv path/to/virtualenv/name_of_virtualenv
$ source path/to/virtualenv/name_of_virtualenv
$ sudo pip3 install -r requirementsNodeConfigApp.txt
						
						
Right now everything you need to run the Node Config App is installed in the virtual environment. To find out how to create a django app please check the tutorial at the official django web page.

But before you have the app up and running you have to star some services first. First you need to download Kafka, then if you want you can change files and do your own configurations. Next, to have the service running you have to do 2 commands.


sudo path/to/bin/zookeeper-server-start.sh config/zookeeper.properties

sudo path/to/bin/kafka-server-start.sh config/server.properties
						


Next to run the app itself another 2 commands need to be done, 1 to effectively run the app and other to run background_tasks to connect with kafka and receive nodes informations.


sudo python3 path/to/manage.py runserver IP:PORT 

sudo python3 path/to/manage.py process_tasks
						
## Switch Controller App

### Overview
The Switch Controller App allows the AMazING admin to turn on or off nodes by enabling or disabling the switch PoE ports. Similarly to Node Config App, Python was choosen to build the app backend with the help of Django framework. For the front end html, css, javascript with jquery and ajax was used.

### Preparing environment

$ sudo apt-get update
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
$ sudo virtualenv path/to/virtualenv/name_of_virtualenv
$ source path/to/virtualenv/name_of_virtualenv
$ sudo pip3 install -r requirementsSwitchControllerApp.txt

						
Finally everything is installed and you can also run the Switch Controlling App in the virtual environment.

To run the app properly and without errors, like the Node Config App you need to have kafka and background-tasks running.



## Notes
If you want to have the two web apps running on the same machine you just need to merge the steps above.

### Preparing environment

$ sudo apt-get update
$ sudo apt-get install python3-pip
$ sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
$ sudo pip3 install virtualenv
$ sudo virtualenv path/to/virtualenv/name_of_virtualenv
$ source path/to/virtualenv/name_of_virtualenv
$ sudo pip3 install -r requirements.txt
						


### requirements.txt content


Django==2.2.1
django-auth-ldap==1.7.0
django-background-tasks==1.2.0
django-crispy-forms==1.7.2
djangorestframework==3.9.2
kafka-python==1.4.6
python-dateutil==2.8.0
python-ldap==3.2.0
requests==2.21.0
						


Since you need to run several things it is better to create a script and use crontab again to make it run at boot or use systemd.


#!/bin/bash

source path/to/virtualenv/name_of_virtualenv

sudo path/to/bin/zookeeper-server-start.sh config/zookeeper.properties & 

sleep 5

sudo path/to/bin/kafka-server-start.sh config/server.properties &

sleep 5

##or
##sudo path/to/bin/kafka-server-start.sh config/server-1.properties &
##sudo path/to/bin/kafka-server-start.sh config/server-2.properties &
##sudo path/to/bin/kafka-server-start.sh config/server-x.properties &
##depending on your needs

sudo python3 /path/to/1stApp/manage.py runserver IP:PORT &

sleep 5

sudo python3 /path/to/1stApp/manage.py process_tasks &

sleep 5

sudo python3 /path/to/2ndApp/manage.py runserver IP:PORT & 

sleep 5

sudo python3 /path/to/2ndApp/manage.py runserver process_tasks &
						


This processes take a bit to initiate so, sleep 5, which means wait 5 seconds let the previous process fully load before a new one start, this is important because some of them depend on each other..

# Tips
1. Virtual environment can be divided in four groups, pip, pip with sudo, pip3 and pip3 with sudo, and all this combinations can have different outcomes when trying to run something. So, make sure you use the same style for installing requirements and running processes, ex, if you installed requests with sudo and pip3, running the app or process without sudo and python3 will not work because it will get requirements from other sub group.

2. Use & at the end of process initialization for making them run in the background. Removes the need of multiple terminals open and allows scripts to initiate multiple processes.

3. Before doing anything in django apps, after requirements instalations or middle app software installation, update settings.py file and run migrations, this will be important especially with background-tasks.

4. If you use different endpoints make sure you change them in every function or requests will trigger exceptions.

5. Always make sure to run zookeeper before running kafka-server. In case you run multiple servers, don't forget to use different ids, ports and log-dirs for each one of them.

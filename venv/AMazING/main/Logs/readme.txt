pip install kafka-python						

bin/zookeeper-server-start.sh config/zookeeper.properties  		// to run zookeeper inside kafka paste

bin/kafka-server-start.sh config/server.properties			// to run kafka server inside kafka paste		

python producer.py

python consumer.py

python verify.py

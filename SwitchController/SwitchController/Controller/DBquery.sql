PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

CREATE TABLE node (
id int PRIMARY KEY,
value varchar(3) NOT NULL,
dateOn date not NULL
);

CREATE TABLE switch (
node_id int,
portId int,
PRIMARY KEY (node_id,portId),
FOREIGN KEY (node_id) REFERENCES node(id)
);


CREATE TABLE alerts (
node_id int,
alert varchar(255),
date_alert date not null,
read varchar(5) not null,
PRIMARY KEY (node_id,alert,date_alert),
FOREIGN KEY (node_id) REFERENCES node(id)
);

CREATE TABLE requests(
node_id int,
requested varchar(5),
PRIMARY KEY (node_id,requested),
FOREIGN KEY (node_id) REFERENCES node(id)
);


CREATE TABLE users (
username varchar(255) PRIMARY KEY,
password varchar(255) not null
);


INSERT INTO node VALUES(1,'OFF','0');
INSERT INTO node VALUES(2,'OFF','0');
INSERT INTO node VALUES(3,'OFF','0');
INSERT INTO node VALUES(4,'OFF','0');
INSERT INTO node VALUES(5,'OFF','0');
INSERT INTO node VALUES(6,'OFF','0');
INSERT INTO node VALUES(7,'OFF','0');
INSERT INTO node VALUES(8,'OFF','0');
INSERT INTO node VALUES(9,'OFF','0');
INSERT INTO node VALUES(10,'OFF','0');
INSERT INTO node VALUES(11,'OFF','0');
INSERT INTO node VALUES(12,'OFF','0');
INSERT INTO node VALUES(13,'OFF','0');
INSERT INTO node VALUES(14,'OFF','0');
INSERT INTO node VALUES(15,'OFF','0');
INSERT INTO node VALUES(16,'OFF','0');
INSERT INTO node VALUES(17,'OFF','0');
INSERT INTO node VALUES(18,'OFF','0');
INSERT INTO node VALUES(19,'OFF','0');
INSERT INTO node VALUES(20,'OFF','0');
INSERT INTO node VALUES(21,'OFF','0');
INSERT INTO node VALUES(22,'OFF','0');
INSERT INTO node VALUES(23,'OFF','0');
INSERT INTO node VALUES(24,'OFF','0');


INSERT INTO switch VALUES(1,1);
INSERT INTO switch VALUES(2,2);
INSERT INTO switch VALUES(3,3);
INSERT INTO switch VALUES(4,4);
INSERT INTO switch VALUES(5,5);
INSERT INTO switch VALUES(6,6);
INSERT INTO switch VALUES(7,7);
INSERT INTO switch VALUES(8,8);
INSERT INTO switch VALUES(9,9);
INSERT INTO switch VALUES(10,10);
INSERT INTO switch VALUES(11,11);
INSERT INTO switch VALUES(12,12);
INSERT INTO switch VALUES(13,13);
INSERT INTO switch VALUES(14,14);
INSERT INTO switch VALUES(15,15);
INSERT INTO switch VALUES(16,16);
INSERT INTO switch VALUES(17,17);
INSERT INTO switch VALUES(18,18);
INSERT INTO switch VALUES(19,19);
INSERT INTO switch VALUES(20,20);
INSERT INTO switch VALUES(21,21);
INSERT INTO switch VALUES(22,22);
INSERT INTO switch VALUES(23,23);
INSERT INTO switch VALUES(24,24);


INSERT INTO users VALUES('AmazingManager','Amazing2019');


COMMIT;

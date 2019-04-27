PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE node(
id int PRIMARY KEY,
value varchar(3) NOT NULL,
color varchar(5) NOT NULL,
portId int NOT NULL);

INSERT INTO node VALUES(1,'OFF','red',1);
INSERT INTO node VALUES(2,'OFF','red',2);
INSERT INTO node VALUES(3,'OFF','red',3);
INSERT INTO node VALUES(4,'OFF','red',4);
INSERT INTO node VALUES(5,'OFF','red',5);
INSERT INTO node VALUES(6,'OFF','red',6);
INSERT INTO node VALUES(7,'OFF','red',7);
INSERT INTO node VALUES(8,'OFF','red',8);
INSERT INTO node VALUES(9,'OFF','red',9);
INSERT INTO node VALUES(10,'OFF','red',10);
INSERT INTO node VALUES(11,'OFF','red',11);
INSERT INTO node VALUES(12,'OFF','red',12);
INSERT INTO node VALUES(13,'OFF','red',13);
INSERT INTO node VALUES(14,'OFF','red',14);
INSERT INTO node VALUES(15,'OFF','red',15);
INSERT INTO node VALUES(16,'OFF','red',16);
INSERT INTO node VALUES(17,'OFF','red',17);
INSERT INTO node VALUES(18,'OFF','red',18);
INSERT INTO node VALUES(19,'OFF','red',19);
INSERT INTO node VALUES(20,'OFF','red',20);
INSERT INTO node VALUES(21,'OFF','red',21);
INSERT INTO node VALUES(22,'OFF','red',22);
INSERT INTO node VALUES(23,'OFF','red',23);
INSERT INTO node VALUES(24,'OFF','red',24);

CREATE TABLE users (
username varchar(255) PRIMARY KEY,
password varchar(255) not null);

INSERT INTO users VALUES('AmazingManager','Amazing2019');

CREATE TABLE alerts (
node_id int,
alert varchar(255),
date_alert date not null,
read boolean not null,
PRIMARY KEY (node_id,alert),
FOREIGN KEY (node_id) REFERENCES node(id));

COMMIT;

DROP DATABASE rosarydb;
CREATE DATABASE rosarydb;
\c rosarydb;
create extension pgcrypto;

DROP ROLE IF EXISTS db_manager; /*Creates a role with a password and appropriate access permissions for each table*/
CREATE ROLE db_manager WITH LOGIN;
ALTER ROLE db_manager WITH PASSWORD 'rosary';

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	id serial PRIMARY KEY,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(40) NOT NULL,
	is_admin BOOLEAN NOT NULL,
	username VARCHAR(24) NOT NULL,
	password TEXT NOT NULL
);
GRANT INSERT, SELECT ON users TO db_manager; /*Should db_manager also have DELETE and/or UPDATE, or should this be an admin-only power?*/
GRANT USAGE, SELECT, UPDATE ON users_id_seq TO db_manager;

drop table if exists customorders; 
create table customorders ( 
	o_id serial primary key,
    user_name varchar(24) NOT NULL,
    hail_mary varchar(70) NOT NULL,
    our_father varchar(70) NOT NULL,
    crucifix varchar(16) NOT NULL,
    center_piece varchar(16) NOT NULL,
    price NUMERIC NOT NULL
);
GRANT INSERT, SELECT, DELETE ON customorders TO db_manager;
GRANT USAGE, SELECT, UPDATE ON customorders_o_id_seq TO db_manager;

drop table if exists payment;
create table payment(
	p_id serial primary key,
	user_name varchar(24) not null,
	first_name varchar(30) NOT NULL,
	last_name varchar(40) NOT NULL,
	home_address text not null, 
	city text not null, 
	state text not null, 
	zipcode text not null,
	card_number text not null,
	o_id bigint,
	foreign key (o_id) references customorders(o_id)
); 
GRANT INSERT, SELECT, DELETE ON payment TO db_manager;
GRANT USAGE, SELECT, UPDATE ON payment_p_id_seq TO db_manager;

DROP TABLE IF EXISTS stock_bead;
CREATE TABLE stock_bead(
	id serial PRIMARY KEY,
	bead_color VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_bead NUMERIC NOT NULL
);
GRANT SELECT, UPDATE ON stock_bead TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_bead_id_seq TO db_manager;

INSERT INTO stock_bead (bead_color, quantity, price_per_bead) VAlUES ('Ruby', 100, 0.50);
INSERT INTO stock_bead (bead_color, quantity, price_per_bead) VAlUES ('Sapphire', 200, 0.50);
INSERT INTO stock_bead (bead_color, quantity, price_per_bead) VAlUES ('Amber', 150, 0.50);
INSERT INTO stock_bead (bead_color, quantity, price_per_bead) VAlUES ('Aquamarine', 225, 0.50);

DROP TABLE IF EXISTS stock_center_piece;
Create table stock_center_piece(
	id serial PRIMARY KEY,
	centerpiece_type VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_center_piece NUMERIC NOT NULL
);
GRANT SELECT, UPDATE ON stock_center_piece TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_center_piece_id_seq TO db_manager;

INSERT INTO stock_center_piece (centerpiece_type, quantity, price_per_center_piece) VALUES ('Titanium', 20, 12.00);
INSERT INTO stock_center_piece (centerpiece_type, quantity, price_per_center_piece) VALUES ('Michael', 40, 10.50);
INSERT INTO stock_center_piece (centerpiece_type, quantity, price_per_center_piece) VALUES ('Virgin Mary', 45, 9.50);

DROP TABLE IF EXISTS stock_crucifix;
Create table stock_crucifix(
	id serial PRIMARY KEY,
	crucifix_type VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_crucifix NUMERIC NOT NULL
);
GRANT SELECT, UPDATE ON stock_crucifix TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_crucifix_id_seq TO db_manager;

INSERT INTO stock_crucifix (crucifix_type, quantity, price_per_crucifix) VALUES ('24k Gold', 20, 11.50);
INSERT INTO stock_crucifix (crucifix_type, quantity, price_per_crucifix) VALUES ('Ruby', 30, 20.00);
INSERT INTO stock_crucifix (crucifix_type, quantity, price_per_crucifix) VALUES ('Silver', 25, 12.85);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
	id serial PRIMARY KEY,
	primary_bead INTEGER REFERENCES stock_bead(id),
	secondary_bead INTEGER REFERENCES stock_bead(id),
	center_piece INTEGER REFERENCES stock_center_piece(id),
	crucifix INTEGER REFERENCES stock_crucifix(id),
	image VARCHAR(128)
);
GRANT INSERT, SELECT ON orders TO db_manager;
GRANT USAGE, SELECT, UPDATE ON orders_id_seq TO db_manager;

INSERT INTO orders (primary_bead, secondary_bead, center_piece, crucifix, image) VALUES (2, 4, 3, 3, 'rosary3.jpg');
INSERT INTO orders (primary_bead, secondary_bead, center_piece, crucifix, image) VALUES (1, 3, 2, 2, 'rosary2.jpg');
INSERT INTO orders (primary_bead, secondary_bead, center_piece, crucifix, image) VALUES (1, 2, 1, 1, 'f_sword.PNG');

DROP TABLE IF EXISTS user_orders;
CREATE TABLE user_orders(
	order_id INTEGER REFERENCES orders(id),
	user_id INTEGER REFERENCES users(id)
);
GRANT INSERT ON user_orders TO db_manager;
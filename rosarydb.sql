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
    user_name varchar(24),
    hail_mary varchar(70),
    our_father varchar(70),
    Crucifix varchar(16),
    center_piece varchar(16),
    price INTEGER
);
GRANT INSERT, SELECT, DELETE ON customorders TO db_manager;
GRANT USAGE, SELECT, UPDATE ON customorders_o_id_seq TO db_manager;

drop table if exists payment;
create table payment(
	p_id serial primary key,
	user_name varchar(24) not null,
	first_name varchar(30),
	last_name varchar(40),
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
	price_per_bead INTEGER NOT NULL
);
GRANT SELECT, UPDATE ON stock_bead TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_bead_id_seq TO db_manager;

DROP TABLE IF EXISTS stock_center_piece;
Create table stock_center_piece(
	id serial PRIMARY KEY,
	centerpiece_type VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_center_piece INTEGER NOT NULL
);
GRANT SELECT, UPDATE ON stock_center_piece TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_center_piece_id_seq TO db_manager;

DROP TABLE IF EXISTS stock_crucifix;
Create table stock_crucifix(
	id serial PRIMARY KEY,
	crucifix_type VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_crucifix INTEGER NOT NULL
);
GRANT SELECT, UPDATE ON stock_crucifix TO db_manager;
GRANT USAGE, SELECT, UPDATE ON stock_crucifix_id_seq TO db_manager;


DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
	id serial PRIMARY KEY,
	primary_bead INTEGER REFERENCES stock_bead(id),
	secondary_bead INTEGER REFERENCES stock_bead(id),
	center_piece INTEGER REFERENCES stock_center_piece(id),
	crucifix INTEGER REFERENCES stock_crucifix(id)
);
GRANT INSERT, SELECT ON orders TO db_manager;
GRANT USAGE, SELECT, UPDATE ON orders_id_seq TO db_manager;

DROP TABLE IF EXISTS user_orders;
CREATE TABLE user_orders(
	order_id INTEGER REFERENCES orders(id),
	user_id INTEGER REFERENCES users(id)
);
GRANT INSERT ON user_orders TO db_manager;
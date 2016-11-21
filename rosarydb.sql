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
GRANT INSERT, SELECT ON users_id_seq TO db_manager;

drop table if exists customorders; 
create table customorders ( 
	o_id serial primary key,
    user_name varchar(24),
    hail_mary varchar(70),
    our_father varchar(70),
    price INTEGER
);
GRANT INSERT, SELECT, DELETE ON customorders TO db_manager;
GRANT INSERT, SELECT, DELETE ON customorders_o_id_seq TO db_manager;

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
GRANT INSERT, SELECT, DELETE ON payment_id_seq TO db_manager;

DROP TABLE IF EXISTS stock;
CREATE TABLE stock(
	id serial PRIMARY KEY,
	bead_color VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_bead INTEGER NOT NULL
);
GRANT SELECT, UPDATE ON stock TO db_manager;
GRANT SELECT, UPDATE ON stock_id_seq TO db_manager;

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
	id serial PRIMARY KEY,
	primary_bead INTEGER REFERENCES stock(id),
	secondary_bead INTEGER REFERENCES stock(id)
);
GRANT INSERT, SELECT ON orders TO db_manager;
GRANT INSERT, SELECT ON orders_id_seq TO db_manager;

DROP TABLE IF EXISTS user_orders;
CREATE TABLE user_orders(
	order_id INTEGER REFERENCES orders(id),
	user_id INTEGER REFERENCES users(id)
);
GRANT INSERT ON user_orders TO db_manager;
DROP DATABASE rosarydb;
CREATE DATABASE rosarydb;
\c rosarydb;
create extension pgcrypto;
CREATE TABLE IF NOT EXISTS users(
	id serial PRIMARY KEY,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(40) NOT NULL,
	is_admin BOOLEAN NOT NULL,
	username VARCHAR(24) NOT NULL,
	password TEXT NOT NULL
);


drop table if exists customorders; 
create table customorders ( 
	o_id serial primary key,
    user_name varchar(24),
    hail_mary varchar(70),
    our_father varchar(70),
    price INTEGER
);

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

	
CREATE TABLE IF NOT EXISTS stock(
	id serial PRIMARY KEY,
	bead_color VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_bead INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS orders(
	id serial PRIMARY KEY,
	primary_bead INTEGER REFERENCES stock(id),
	secondary_bead INTEGER REFERENCES stock(id)
);


CREATE TABLE IF NOT EXISTS user_orders(
	order_id INTEGER REFERENCES orders(id),
	user_id INTEGER REFERENCES users(id)
);
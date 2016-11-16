DROP DATABASE rosarydb;
CREATE DATABASE rosarydb;
\c rosarydb;

CREATE TABLE IF NOT EXISTS users(
	id integer PRIMARY KEY,
	first_name VARCHAR(30) NOT NULL,
	last_name VARCHAR(40) NOT NULL,
	is_admin BOOLEAN NOT NULL,
	username VARCHAR(24) NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock(
	id INTEGER PRIMARY KEY,
	bead_color VARCHAR(16) NOT NULL,
	quantity INTEGER NOT NULL,
	price_per_bead INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS orders(
	id INTEGER PRIMARY KEY,
	primary_bead INTEGER REFERENCES stock(id),
	secondary_bead INTEGER REFERENCES stock(id)
);

CREATE TABLE IF NOT EXISTS user_orders(
	order_id INTEGER REFERENCES orders(id),
	user_id INTEGER REFERENCES users(id)
);
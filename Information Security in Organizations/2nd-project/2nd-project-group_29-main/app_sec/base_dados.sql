CREATE DATABASE base_dados.db;

CREATE TABLE accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    secret TEXT NOT NULL
);


CREATE TABLE memorabilia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    stock INTEGER,
    price DOUBLE NOT NULL
);

CREATE TABLE cart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    memorabilia_id INTEGER NOT NULL
);


CREATE TABLE comments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    comment TEXT NOT NULL
);
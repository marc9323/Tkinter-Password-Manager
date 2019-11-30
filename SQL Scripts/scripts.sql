/*
Marc Holman
CIS 2531 Term Project

Tkinter Password Manager Application

SQLITE Scripts for Table Creation:
-- users
-- links

 */

-- enable foreign key constraints for sqlite3
 PRAGMA foreign_keys = ON;

 -- create table users
 create table users
(
    id INTEGER not null
        primary key autoincrement,
    email    TEXT not null unique, -- email is the unique identifier for username
    password TEXT not null
);

create table links
(
    id INTEGER not null
        primary key autoincrement,
    user_id   INTEGER,
    site_name TEXT,
    username  TEXT,
    url       TEXT,
    note      TEXT,
    password  TEXT,
    security  TEXT,
    email     TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
    ON DELETE CASCADE -- when a user is deleted, the links for that user are also deleted
);
create table listeners
(
    id       int auto_increment
        primary key,
    username varchar(64) not null,
    email    varchar(64) not null,
    password varchar(64) not null,
    constraint listeners_email_uindex
        unique (email),
    constraint listeners_username_uindex
        unique (username)
);

INSERT INTO DBtify.listeners (id, username, email, password) VALUES (1, 'selenparlar', 'parlarselen@gmail.com', '1234');
INSERT INTO DBtify.listeners (id, username, email, password) VALUES (2, 'taflangundem', 'gundem@boun.edu.tr', '1234');
INSERT INTO DBtify.listeners (id, username, email, password) VALUES (3, 'can', 'can@gmail.com', '1234');
INSERT INTO DBtify.listeners (id, username, email, password) VALUES (4, 'pelin', 'pelin@gmail.com', '1234');
INSERT INTO DBtify.listeners (id, username, email, password) VALUES (5, 'daniel_ek', 'daniel@spotify.com', '1234');
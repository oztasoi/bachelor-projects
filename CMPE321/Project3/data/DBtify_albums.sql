create table albums
(
    id    int auto_increment
        primary key,
    genre varchar(64)      not null,
    title varchar(64)      not null,
    likes bigint default 0 not null
);

INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (1, 'Pop', 'Allahaismarladik', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (2, 'Rock', 'Yollar Bizi Bekler', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (4, 'Pop', 'Tuna Kiremitci ve Arkadaslari, Vol. 2', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (7, 'Pop', 'DEMO', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (9, 'Rock', 'Point of Know Return', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (10, 'Rock', 'The Game', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (11, 'Rock', 'News Of The World', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (13, 'Rock', 'Out Of Time', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (14, 'Pop', 'Soluk', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (15, 'Pop', 'Cahille Sohbeti Kestim', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (16, 'Pop', 'Yadigar', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (17, 'Abdallik', 'Gonul Dagi', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (18, 'Alternative', 'Sehri Huzun', 0);
INSERT INTO DBtify.albums (id, genre, title, likes) VALUES (19, 'Rock', 'Geldiler', 0);
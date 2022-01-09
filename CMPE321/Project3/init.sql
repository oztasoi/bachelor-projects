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

create table songs
(
    id    int auto_increment
        primary key,
    title varchar(64)      not null,
    likes bigint default 0 not null
);

INSERT INTO DBtify.songs (id, title, likes) VALUES (10, 'Kusura Bakma', 3);
INSERT INTO DBtify.songs (id, title, likes) VALUES (20, 'Gor Beni', 2);
INSERT INTO DBtify.songs (id, title, likes) VALUES (40, 'Balkan Kizi', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (41, 'Seninle Her Sey Olur', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (70, 'Begonvil', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (90, 'Dust In The World', 4);
INSERT INTO DBtify.songs (id, title, likes) VALUES (100, 'Another One Bites The Dust', 2);
INSERT INTO DBtify.songs (id, title, likes) VALUES (110, 'We Will Rock You', 2);
INSERT INTO DBtify.songs (id, title, likes) VALUES (130, 'Losing My Religion', 5);
INSERT INTO DBtify.songs (id, title, likes) VALUES (140, 'Gonul Dagi', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (141, 'Nazima', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (150, 'Farketmeden', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (160, 'Farketmeden', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (170, 'Gonul Dagi', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (180, 'Dunyanin Sonuna Dogmusum', 1);
INSERT INTO DBtify.songs (id, title, likes) VALUES (190, 'Ali Desidero', 0);

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

create table artists
(
    id       int auto_increment
        primary key,
    name     varchar(64) not null,
    surname  varchar(64) null,
    password varchar(64) not null
);

INSERT INTO DBtify.artists (id, name, surname, password) VALUES (3, 'Ceylan', 'Ertem', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (4, 'Fikret', 'Kizilok', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (5, 'Kansas', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (6, 'Manga', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (7, 'MFO', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (8, 'Neset', 'Ertas', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (9, 'Pinhani', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (10, 'Queen', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (11, 'R.E.M', null, '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (12, 'Sezen', 'Aksu', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (13, 'Tuna', 'Kiremitci', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (14, 'Coskun', 'Karademir', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (15, 'Mert Fehmi', 'Alatan', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (16, 'Berkant', 'Celen', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (17, 'Alp', 'Ersonmez', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (18, 'Can', 'Gungor', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (19, 'Cihan', 'Murtazaoglu', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (20, 'Eliz', 'Dubaz', '1234');
INSERT INTO DBtify.artists (id, name, surname, password) VALUES (21, 'Esin', 'Iris', '1234');

create table album_artist_relation
(
    id         int auto_increment
        primary key,
    album_id   int not null,
    artist_id  int not null,
    is_creator tinyint(1) default 0 not null
);

INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (1, 14, 3);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (2, 15, 3);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (3, 16, 4);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (4, 9, 5);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (5, 18, 6);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (6, 19, 7);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (7, 17, 8);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (8, 2, 9);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (9, 10, 10);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (10, 11, 10);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (11, 13, 11);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (12, 1, 12);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (13, 7, 12);
INSERT INTO DBtify.album_artist_relation (id, album_id, artist_id) VALUES (14, 4, 13);

create table album_song_relation
(
    id       int auto_increment
        primary key,
    album_id int not null,
    song_id  int not null
);

INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (1, 14, 140);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (2, 14, 141);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (3, 15, 150);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (4, 16, 160);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (5, 9, 90);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (6, 18, 180);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (7, 19, 10);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (8, 17, 170);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (9, 2, 20);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (10, 10, 100);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (11, 11, 110);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (12, 13, 130);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (13, 1, 10);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (14, 7, 70);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (15, 4, 40);
INSERT INTO DBtify.album_song_relation (id, album_id, song_id) VALUES (16, 4, 41);

create table artist_song_relation
(
    id         int auto_increment
        primary key,
    artist_id  int                  not null,
    song_id    int                  not null,
    is_creator tinyint(1) default 0 not null
);

INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (1, 3, 140, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (2, 3, 141, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (3, 14, 140, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (4, 15, 140, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (5, 16, 140, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (6, 17, 140, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (7, 18, 140, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (8, 19, 141, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (9, 17, 141, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (10, 18, 141, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (11, 18, 150, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (12, 20, 40, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (13, 21, 41, 0);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (14, 4, 160, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (15, 5, 90, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (16, 6, 180, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (17, 7, 190, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (18, 8, 170, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (19, 9, 20, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (20, 10, 100, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (21, 10, 110, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (22, 11, 130, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (23, 12, 10, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (24, 12, 70, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (25, 13, 40, 1);
INSERT INTO DBtify.artist_song_relation (id, artist_id, song_id, is_creator) VALUES (26, 13, 41, 1);

create table listener_album_relation
(
    id          int auto_increment
        primary key,
    album_id    int not null,
    listener_id int not null
);

INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (1, 4, 1);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (2, 1, 1);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (3, 9, 1);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (4, 13, 1);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (5, 14, 1);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (6, 9, 2);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (7, 1, 2);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (8, 13, 2);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (9, 9, 3);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (10, 13, 3);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (11, 14, 3);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (12, 15, 3);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (13, 1, 4);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (14, 7, 4);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (15, 13, 4);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (16, 9, 5);
INSERT INTO DBtify.listener_album_relation (id, album_id, listener_id) VALUES (17, 13, 5);

create table listener_song_relation
(
    id          int auto_increment
        primary key,
    song_id     int not null,
    listener_id int not null
);

INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (1, 40, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (2, 10, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (3, 130, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (4, 20, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (5, 41, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (6, 90, 1);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (7, 90, 2);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (8, 110, 2);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (9, 100, 2);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (10, 130, 2);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (11, 10, 2);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (12, 130, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (13, 140, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (14, 141, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (15, 150, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (16, 160, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (17, 170, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (18, 90, 3);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (19, 180, 4);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (20, 20, 4);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (21, 10, 4);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (22, 70, 4);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (23, 130, 4);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (24, 90, 5);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (25, 110, 5);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (26, 100, 5);
INSERT INTO DBtify.listener_song_relation (id, song_id, listener_id) VALUES (27, 130, 5);

create trigger delete_album_and_songs
    after delete on albums
    for each row
    begin
        delete from artist_song_relation where song_id in (select song_id from album_song_relation where album_id = OLD.id);
        delete from songs where id in (select song_id from album_song_relation where album_id = OLD.id);
        delete from album_song_relation where album_id = OLD.id;
        delete from listener_album_relation where album_id = OLD.id;
        delete from album_artist_relation where album_id = OLD.id;
    end;

create trigger delete_song_and_like
    after delete on songs
    for each row
    begin
        delete from listener_song_relation where song_id = OLD.id;
    end;

create trigger create_like_album_song
    after insert on listener_album_relation
    for each row
    begin
        update songs
        set likes = likes + 1
        where id in (select song_id from album_song_relation where album_song_relation.album_id = NEW.album_id);
    end;

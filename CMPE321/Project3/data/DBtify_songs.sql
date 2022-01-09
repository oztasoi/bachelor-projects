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
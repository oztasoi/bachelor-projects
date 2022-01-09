create table album_artist_relation
(
    id        int auto_increment
        primary key,
    album_id  int not null,
    artist_id int not null
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
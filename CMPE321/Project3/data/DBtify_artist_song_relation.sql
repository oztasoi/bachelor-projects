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
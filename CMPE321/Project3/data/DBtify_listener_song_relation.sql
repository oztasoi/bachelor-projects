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
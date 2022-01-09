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
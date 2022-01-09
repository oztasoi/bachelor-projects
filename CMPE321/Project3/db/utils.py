class Artists:

    @staticmethod
    def get_artists_query():
        return "select * from artists;"

    @staticmethod
    def get_active_artists_query():
        return "select * from artists where id in (select artist_id from artist_song_relation where is_creator = 1);"

    @staticmethod
    def get_artist_query_by_id(id):
        return f"select * from artists where id = {id};"

    @staticmethod
    def get_artist_query_by_name(name):
        return f"select * from artists where name = \"{name}\";"

    @staticmethod
    def get_artist_query_by_surname(surname):
        return f"select * from artists where surname = \"{surname}\";"

    @staticmethod
    def get_artist_query_by_name_by_surname(credentials):
        return f"select * from artists where name = \"{credentials['name']}\" and surname = \"{credentials['surname']}\";"

    @staticmethod
    def post_single_artist_query(artist):
        return f"insert into artists (name, surname, password) values (\"{artist['name']}\", \"{artist['surname']}\", \"{artist['password']}\");"

    @staticmethod
    def update_artist_query(artist):
        return f"update artists set name={artist['name']}, surname={artist['surname']}, password={artist['password']} where id={artist['id']};"

    @staticmethod
    def delete_single_artist_query(id):
        return f"delete from artists where id={id};"

    @staticmethod
    def delete_all_artists_query():
        return "delete from artists;"

class Listeners:
    
    @staticmethod
    def get_listeners_query():
        return "select * from listeners;"
    
    @staticmethod
    def get_listener_query_by_id(id):
        return f"select * from listeners where id = \"{id}\";"
    
    @staticmethod
    def get_listener_query_by_username(username):
        return f"select * from listeners where username = \"{username}\";"
    
    @staticmethod
    def get_listener_query_by_email(email):
        return f"select * from listeners where email = \"{email}\";"

    @staticmethod
    def get_listener_query_by_username_by_email(credentials):
        return f"select * from listeners where email = \"{credentials['email']}\" and username = \"{credentials['username']}\";"

    @staticmethod
    def post_single_listener_query(listener):
        return f"insert into listeners (username, email, password) values (\"{listener['username']}\", \"{listener['email']}\", \"{listener['password']}\");"

    @staticmethod
    def delete_single_listener_query(id):
        return f"delete from listeners where id = \"{id}\";"

    @staticmethod
    def delete_all_listeners():
        return f"delete from listeners;"

class Albums:

    @staticmethod
    def get_albums_query():
        return f"select * from albums;"

    @staticmethod
    def get_album_likes(album_id):
        return f"select likes from albums where id = \"{album_id}\";"

    @staticmethod
    def get_album_single_query(id):
        return f"select * from albums where id = {id};"

    @staticmethod
    def get_albums_query_by_genre(genre):
        return f"select * from albums where genre = {genre};"

    @staticmethod
    def get_albums_query_by_title(title):
        return f"select * from albums where title = {title};"

    @staticmethod
    def get_unliked_songs_from_album_of_listener_query(relation):
        return f"select distinct song_id from (select song_id from album_song_relation inner join (select * from songs where id in (select song_id from album_song_relation inner join (select album_id from listener_album_relation where listener_id = \"{relation['listener_id']}\") tmp on album_song_relation.album_id = tmp.album_id)) tmp2 on song_id = tmp2.id where album_id = \"{relation['album_id']}\") tmp3 where song_id not in (select song_id from listener_song_relation where listener_id = \"{relation['listener_id']}\");"

    @staticmethod
    def post_single_album_query(album):
        return f"insert into albums (genre, title) values (\"{album['genre']}\", \"{album['title']}\");"

    @staticmethod
    def delete_single_album_query(id):
        return f"delete from albums where id = {id};"

    @staticmethod
    def delete_all_albums():
        return f"delete from albums;"

    @staticmethod
    def update_album_query(album):
        return f"update albums set genre = \"{album['genre']}\", title = \"{album['title']}\" where id = \"{album['id']}\";"

    @staticmethod
    def increment_like(album_id):
        return f"update albums set likes = likes + 1 where id = \"{album_id}\";"

    @staticmethod
    def decrement_like(album_id):
        return f"update albums set likes = likes - 1 where id = \"{album_id}\";"

    @staticmethod
    def get_songs_in_albums(album_id):
        return f"select * from songs where id in (select song_id from album_song_relation where album_id = \"{album_id}\");"

class Songs:

    @staticmethod
    def get_songs_query():
        return f"select * from songs;"

    @staticmethod
    def get_song_likes_query(song_id):
        return f"select likes from songs where id = \"{song_id}\""

    @staticmethod
    def get_single_song_query_by_id(song_id):
        return f"select * from songs where id = {song_id};"

    @staticmethod
    def get_single_song_query_by_title(song_title):
        return f"select * from songs where title = {song_title};"

    @staticmethod
    def get_songs_by_keyword_query(keyword):
        return f"select * from songs where instr(title, \"{keyword}\") > 0;"

    @staticmethod
    def post_single_song_query(song):
        return f"insert into songs (title, likes) values (\"{song['title']}\", \"{int(0)}\");"

    @staticmethod
    def delete_single_song_query(song_id):
        return f"delete from songs where id = {song_id};"

    @staticmethod
    def delete_all_songs():
        return f"delete from songs;"

    @staticmethod
    def update_song_query(song):
        return f"update songs set title = \"{song['title']}\" where id = \"{song['id']}\";"

    @staticmethod
    def increment_like(song_id):
        return f"update songs set likes = likes + 1 where id = {song_id};"

    @staticmethod
    def decrement_like(song_id):
        return f"update songs set likes = likes - 1 where id = {song_id};"

class AlbumArtistRelations:

    @staticmethod
    def get_album_artist_relations_query():
        return f"select * from album_artist_relation;"

    @staticmethod
    def get_album_artist_relation_query_by_album_id(album_id):
        return f"select * from artists where id in (select artist_id from album_artist_relation where album_id = \"{album_id}\");"

    @staticmethod
    def get_album_artist_relation_query_by_artist_id(artist_id):
        return f"select * from albums where id in (select album_id from album_artist_relation where artist_id = \"{artist_id}\");"

    @staticmethod
    def post_single_album_artist_relation_query(relation):
        return f"insert into album_artist_relation (album_id, artist_id, is_creator) values (\"{relation['album_id']}\", \"{relation['artist_id']}\", \"{relation['is_creator']}\");"

    @staticmethod
    def delete_album_artist_relation_by_album_id(album_id):
        return f"delete from album_artist_relation where album_id = {album_id};"

    @staticmethod
    def delete_album_artist_relation_by_artist_id(artist_id):
        return f"delete from album_artist_relation where artist_id = {artist_id};"

    @staticmethod
    def delete_album_artist_relation_query(relation):
        return f"delete from album_artist_relation where artist_id = \"{relation['artist_id']}\" and album_id = \"{relation['album_id']}\" ;"

class ArtistSongRelations:

    @staticmethod
    def get_artist_song_relations_query():
        return f"select * from artist_song_relation;"

    @staticmethod
    def get_artist_song_relation_query_by_artist_id_all(artist_id):
        return f"select * from songs where id in (select song_id from artist_song_relation where artist_id = \"{artist_id}\");"

    @staticmethod
    def get_artist_song_relation_query_by_artist_id(artist_id):
        return f"select * from songs where id in (select song_id from artist_song_relation where artist_id = \"{artist_id}\" and is_creator = \"{1}\");"

    @staticmethod
    def get_artist_song_relation_query_by_song_id(song_id):
        return f"select * from artists where id in (select artist_id from artist_song_relation where song_id = \"{song_id}\");"

    @staticmethod
    def get_popular_song_of_an_artist_query_by_artist_id(artist_id):
        return f"select * from songs where id in (select song_id from artist_song_relation where artist_id = \"{artist_id}\" ) order by -likes;"

    @staticmethod
    def post_single_artist_song_relation_query_with_owner(relation):
        return f"insert into artist_song_relation (artist_id, song_id, is_creator) values (\"{relation['artist_id']}\", \"{relation['song_id']}\", \"{relation['is_creator']}\");"

    @staticmethod
    def post_single_artist_song_relation_query(relation):
        return f"insert into artist_song_relation (artist_id, song_id) values (\"{relation['artist_id']}\", \"{relation['song_id']}\");"

    @staticmethod
    def delete_artist_song_relation_query_by_artist_id(artist_id):
        return f"delete from artist_song_relation_where artist_id = {artist_id};"

    @staticmethod
    def delete_artist_song_relation_query_by_song_id(song_id):
        return f"delete from artist_song_relation where song_id = {song_id};"

    @staticmethod
    def delete_artist_song_relation_query(relation):
        return f"delete from artist_song_relation where song_id = \"{relation['song_id']}\" and artist_id = \"{relation['artist_id']}\";"

class AlbumSongRelations:

    @staticmethod
    def get_album_song_relations_query():
        return f"select * from album_song_relation;"

    @staticmethod
    def get_album_song_relation_query_by_album_id(album_id):
        return f"select * from album_song_relation where album_id = {album_id};"

    @staticmethod
    def get_album_song_relation_query_by_song_id(song_id):
        return f"select * from album_song_relation where song_id = {song_id};"

    @staticmethod
    def get_song_from_genre_query_by_genre(genre):
        return f"select * from songs where id in (select song_id from album_song_relation where album_id in (select id from albums where genre = \"{genre}\"));"

    @staticmethod
    def post_album_song_relation_query(relation):
        return f"insert into album_song_relation (album_id, song_id) values (\"{relation['album_id']}\", \"{relation['song_id']}\");"

    @staticmethod
    def delete_album_song_relation_query_by_album_id(album_id):
        return f"delete from album_song_relation where album_id = {album_id};"

    @staticmethod
    def delete_album_song_relation_query_by_song_id(song_id):
        return f"delete from album_song_relation where song_id = {song_id};"

    @staticmethod
    def delete_album_song_relation_query(relation):
        return f"delete from album_song_relation where album_id = \"{relation['album_id']}\" and song_id = \"{relation['song_id']}\" ;"

class ListenerSongRelations:

    @staticmethod
    def get_liked_songs_query(listener_id):
        return f"select * from songs where id in (select song_id from listener_song_relation where listener_id = \"{listener_id}\");"

    @staticmethod
    def get_liked_song_query_by_relation(relation):
        return f"select * from listener_song_relation where listener_id = \"{relation['listener_id']}\" and song_id = \"{relation['song_id']}\";"

    @staticmethod
    def post_liked_song_relation_query(relation):
        return f"insert into listener_song_relation (song_id, listener_id) values (\"{relation['song_id']}\", \"{relation['listener_id']}\");"

    @staticmethod
    def delete_liked_song_relation_query(relation):
        return f"delete from listener_song_relation where song_id = \"{relation['song_id']}\" and listener_id = \"{relation['listener_id']}\";"

class ListenerAlbumRelations:

    @staticmethod
    def get_liked_albums_query(listener_id):
        return f"select * from albums where id in (select album_id from listener_album_relation where listener_id = \"{listener_id}\");"

    @staticmethod
    def get_liked_album_query_by_relation(relation):
        return f"select * from listener_album_relation where listener_id = \"{relation['listener_id']}\" and album_id = \"{relation['album_id']}\";"

    @staticmethod
    def post_liked_album_relation_query(relation):
        return f"insert into listener_album_relation (album_id, listener_id) values (\"{relation['album_id']}\", \"{relation['listener_id']}\");"

    @staticmethod
    def delete_liked_album_relation_query(relation):
        return f"delete from listener_album_relation where album_id = \"{relation['album_id']}\" and listener_id = \"{relation['listener_id']}\" ;"

class Generals:

    @staticmethod
    def get_last_insert_id(table_name):
        return f"select max(id) from {table_name};"

class StoredProcedures:

    @staticmethod
    def get_coworkers_by_stored():
        return f"create procedure get_coworkers(in s_id int)\nbegin\n\tselect * from artists where id in (select artist_id from artist_song_relation where song_id = s_id);\nend;"

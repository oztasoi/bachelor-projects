from http import HTTPStatus

from flask import request
from flask_restful import Resource

from db.helper import DBHelper
from db.utils import Songs, Generals, AlbumSongRelations, ListenerSongRelations, Albums, ListenerAlbumRelations

class SongsResource(Resource):

    def get(self):
        return DBHelper.run_query(Songs.get_songs_query()), HTTPStatus.OK

    def post(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Songs.post_single_song_query(body))
            id = DBHelper.run_query(Generals.get_last_insert_id("songs"))

            relation = {}
            relation['song_id'] = id[0]['max(id)']
            relation['album_id'] = body['album_id']

            DBHelper.run_query(AlbumSongRelations.post_album_song_relation_query(relation))
            return { "msg" : "Creating song operation successful." }, HTTPStatus.CREATED
        except Exception:
            return { "msg" : "Creating song operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Songs.delete_single_song_query(body['id']))
            album_id = DBHelper.run_query(AlbumSongRelations.get_album_song_relation_query_by_song_id(body['id']))[0]['album_id']
            relation = {}
            relation['song_id'] = body['id']
            relation['album_id'] = album_id
            DBHelper.run_query(AlbumSongRelations.delete_album_song_relation_query(relation))
            return { "msg" : "Deleting song operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting song operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def patch(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Songs.update_song_query(body))
            return { "msg" : "Updating song operation successful." }, HTTPStatus.OK
        except:
            return { "msg" : "Updating song operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class SongLikesResource(Resource):

    def get(self, song_id):
        try:
            return DBHelper.run_query(Songs.get_song_likes_query(song_id))[0], HTTPStatus.OK
        except Exception:
            pass

    def post(self, song_id):
        body = request.get_json(force=True)
        try:
            relation = {}
            relation['listener_id'] = body['listener_id']
            relation['song_id'] = song_id
            is_liked = DBHelper.run_query(ListenerSongRelations.get_liked_song_query_by_relation(relation))
            if len(is_liked) == 0:
                album_id = DBHelper.run_query(AlbumSongRelations.get_album_song_relation_query_by_song_id(song_id))[0]['album_id']
                DBHelper.run_query(Songs.increment_like(song_id))
                relation = {"listener_id" : body['listener_id'], "album_id" : album_id}
                DBHelper.run_query(ListenerSongRelations.post_liked_song_relation_query(relation)), HTTPStatus.OK
                is_album_empty = DBHelper.run_query(Albums.get_unliked_songs_from_album_of_listener_query(relation))
                if len(is_album_empty) == 0:
                    DBHelper.run_query(ListenerAlbumRelations.post_liked_album_relation_query(relation))
                    return DBHelper.run_query(Albums.increment_like(album_id)), HTTPStatus.OK
        except Exception:
            pass

    def delete(self, song_id):
        body = request.get_json(force=True)
        try:
            relation = {}
            relation['listener_id'] = body['listener_id']
            relation['song_id'] = song_id
            is_disliked = DBHelper.run_query(ListenerSongRelations.get_liked_song_query_by_relation(relation))
            if len(is_disliked) > 0:
                album_id = DBHelper.run_query(AlbumSongRelations.get_album_song_relation_query_by_song_id(song_id))[0]['album_id']
                DBHelper.run_query(Songs.decrement_like(song_id))
                DBHelper.run_query(ListenerSongRelations.delete_liked_song_relation_query(relation))
                relation = {"listener_id" : body['listener_id'], "album_id" : album_id}
                songs_in_album = DBHelper.run_query(AlbumSongRelations.get_album_song_relation_query_by_album_id(album_id))
                is_album_empty = DBHelper.run_query(Albums.get_unliked_songs_from_album_of_listener_query(relation))
                if len(is_album_empty) == len(songs_in_album):
                    DBHelper.run_query(ListenerAlbumRelations.delete_liked_album_relation_query(relation))
                    return DBHelper.run_query(Albums.decrement_like(album_id)), HTTPStatus.OK
        except Exception:
            pass

class SongSearchByGenreResource(Resource):

    def get(self, genre):
        return DBHelper.run_query(AlbumSongRelations.get_song_from_genre_query_by_genre(genre)), HTTPStatus.OK

class SongSearchByKeywordResource(Resource):

    def get(self, keyword):
        return DBHelper.run_query(Songs.get_songs_by_keyword_query(keyword)), HTTPStatus.OK


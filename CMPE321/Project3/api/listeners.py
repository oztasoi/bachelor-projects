from http import HTTPStatus

from flask import request
from flask_restful import Resource

from db.helper import DBHelper
from db.utils import Albums, Songs, ListenerSongRelations, ListenerAlbumRelations

class ListenerSongsResource(Resource):

    def get(self, listener_id):
        return DBHelper.run_query(ListenerSongRelations.get_liked_songs_query(listener_id)), HTTPStatus.OK

    def post(self, listener_id):
        try:
            body = request.get_json(force=True)
            relation = {}
            relation['song_id'] = body['song_id']
            relation['listener_id'] = listener_id
            DBHelper.run_query(ListenerSongRelations.post_liked_song_relation_query(relation))
            DBHelper.run_query(Songs.increment_like(relation['song_id']))
            return { "msg" : "Creating liked song operation successful." }, HTTPStatus.ACCEPTED
        except Exception:
            return { "msg" : "Creating liked song operation FAILED!" }, HTTPStatus.BAD_REQUEST

    def delete(self, listener_id):
        try:
            body = request.get_json(force=True)
            relation = {}
            relation['song_id'] = body['song_id']
            relation['listener_id'] = listener_id
            DBHelper.run_query(ListenerSongRelations.delete_liked_song_relation_query(relation))
            DBHelper.run_query(Songs.decrement_like(relation['song_id']))
            return { "msg" : "Deleting liked song operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting liked song operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class ListenerAlbumsResource(Resource):

    def get(self, listener_id):
        return DBHelper.run_query(ListenerAlbumRelations.get_liked_albums_query(listener_id)), HTTPStatus.OK

    def post(self, listener_id):
        try:
            body = request.get_json(force=True)
            relation = {}
            relation['album_id'] = body['album_id']
            relation['listener_id'] = listener_id
            DBHelper.run_query(ListenerAlbumRelations.post_liked_album_relation_query(relation))
            DBHelper.run_query(Albums.increment_like(relation['album_id']))
            songs = DBHelper.run_query(Albums.get_songs_in_albums(relation['album_id']))
            for song in songs:
                song_relation = {}
                song_relation['song_id'] = song['id']
                song_relation['listener_id'] = listener_id
                DBHelper.run_query(ListenerSongRelations.post_liked_song_relation_query(song_relation))
                DBHelper.run_query(Songs.increment_like(song['id']))
            return { "msg" : "Creating liked album operation successful." }, HTTPStatus.ACCEPTED
        except Exception:
            return { "msg" : "Creating liked album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self, listener_id):
        try:
            body = request.get_json(force=True)
            relation = {}
            relation['album_id'] = body['album_id']
            relation['listener_id'] = listener_id
            DBHelper.run_query(ListenerAlbumRelations.delete_liked_album_relation_query(relation))
            DBHelper.run_query(Albums.decrement_like(relation['album_id']))
            songs = DBHelper.run_query(Albums.get_songs_in_albums(relation['album_id']))
            for song in songs:
                song_relation = {}
                song_relation['song_id'] = song['id']
                song_relation['listener_id'] = listener_id
                DBHelper.run_query(ListenerSongRelations.delete_liked_song_relation_query(song_relation))
                DBHelper.run_query(Songs.decrement_like(song['id']))
            return { "msg" : "Deleting liked album operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting liked album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

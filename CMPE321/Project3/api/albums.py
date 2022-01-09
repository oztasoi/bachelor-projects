from http import HTTPStatus

from flask import request
from flask_restful import Resource

from db.helper import DBHelper
from db.utils import Albums, Songs, ListenerSongRelations, ListenerAlbumRelations, AlbumSongRelations

class AlbumsResource(Resource):

    def get(self):
        return DBHelper.run_query(Albums.get_albums_query()), HTTPStatus.OK
    
    def post(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Albums.post_single_album_query(body))
            return { "msg" : "Creating album operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Creating album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST
    
    def delete(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Albums.delete_single_album_query(body['id']))
            return { "msg" : "Deleting album operation successful." }, HTTPStatus.CREATED
        except Exception:
            return { "msg" : "Deleting album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def patch(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Albums.update_album_query(body))
            return { "msg" : "Updating album operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Updating album operatio FAILED!!!" }, HTTPStatus.BAD_REQUEST

class AlbumLikesResource(Resource):

    def get(self, album_id):
        return DBHelper.run_query(Albums.get_album_likes(album_id))[0], HTTPStatus.OK

    def post(self, album_id):
        body = request.get_json(force=True)
        try:
            relation = {}
            relation['listener_id'] = body['listener_id']
            relation['album_id'] = album_id
            is_album_liked = DBHelper.run_query(ListenerAlbumRelations.get_liked_album_query_by_relation(relation))
            if len(is_album_liked) == 0:
                DBHelper.run_query(ListenerAlbumRelations.post_liked_album_relation_query(relation))
                DBHelper.run_query(Albums.increment_like(album_id))
            songs = DBHelper.run_query(Albums.get_unliked_songs_from_album_of_listener_query(relation))
            for song in songs:
                relation = {}
                relation['listener_id'] = body['listener_id']
                relation['song_id'] = song['song_id']
                DBHelper.run_query(Songs.increment_like(song['song_id']))
                DBHelper.run_query(ListenerSongRelations.post_liked_song_relation_query(relation))
            return { "msg" : "Album like operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Album like operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self, album_id):
        body = request.get_json(force=True)
        try:
            DBHelper.run_query(Albums.decrement_like(album_id))
            relation = {}
            relation['album_id'] = album_id
            relation['listener_id'] = body['listener_id']
            DBHelper.run_query(ListenerAlbumRelations.delete_liked_album_relation_query(relation))
            songs = DBHelper.run_query(Albums.get_songs_in_albums(album_id))
            for song in songs:
                relation = {}
                relation['song_id'] = song['id']
                relation['listener_id'] = body['listener_id']
                DBHelper.run_query(Songs.decrement_like(song['id']))
                DBHelper.run_query(ListenerSongRelations.delete_liked_song_relation_query(relation))
            return { "msg" : "Album dislike operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Album dislike operation FAILED!!!" }, HTTPStatus.BAD_GATEWAY

class AlbumSongsResource(Resource):

    def get(self, album_id):
        return DBHelper.run_query(Albums.get_songs_in_albums(album_id)), HTTPStatus.OK
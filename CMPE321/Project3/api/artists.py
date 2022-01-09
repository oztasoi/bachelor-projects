from http import HTTPStatus

from flask import request
from flask import current_app
from flask_mysqldb import MySQL
from flask_restful import Resource

from db.helper import DBHelper
from db.utils import Albums, Songs, Generals, StoredProcedures, ArtistSongRelations, AlbumArtistRelations, AlbumSongRelations, Artists

class ArtistAlbumsResource(Resource):

    def get(self, artist_id):
        return DBHelper.run_query(AlbumArtistRelations.get_album_artist_relation_query_by_artist_id(artist_id)), HTTPStatus.OK

    def post(self, artist_id):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Albums.post_single_album_query(body))
            id = DBHelper.run_query(Generals.get_last_insert_id("albums"))

            relation = {}
            relation['album_id'] = id[0]['max(id)']
            relation['artist_id'] = artist_id
            relation['is_creator'] = body['is_creator']

            DBHelper.run_query(AlbumArtistRelations.post_single_album_artist_relation_query(relation))
            return { "msg" : "Creating artist album operation successful." }, HTTPStatus.CREATED
        except Exception:
            return { "msg" : "Creating artist album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self, artist_id):
        body = request.get_json(force=True)

        if body['is_creator'] == False:
            return { "msg" : "Ownership is not found. Abort delete operation!!!" }, HTTPStatus.BAD_REQUEST

        DBHelper.run_query(Albums.delete_single_album_query(body['album_id']))
        songs = DBHelper.run_query(Albums.get_songs_in_albums(body['album_id']))
        for song in songs:
            DBHelper.run_query(Songs.delete_single_song_query(song['id']))

            artist_song_relation = {}
            artist_song_relation['artist_id'] = artist_id
            artist_song_relation['song_id'] = song['id']
            album_song_relation = {}
            album_song_relation['song_id'] = song['id']
            album_song_relation['album_id'] = body['album_id']

            DBHelper.run_query(ArtistSongRelations.delete_artist_song_relation_query(artist_song_relation))
            DBHelper.run_query(AlbumSongRelations.delete_album_song_relation_query(album_song_relation))

        DBHelper.run_query(AlbumArtistRelations.delete_album_artist_relation_by_album_id(body['album_id']))
        return { "msg" : "Deleting artist album operation successful." }, HTTPStatus.OK

    def patch(self, artist_id):
        body = request.get_json(force=True)
        if body['is_creator'] == 1:
            return { "msg" : "Ownership demand prevented.It is forbidden in our platform. Aborted!!!" }, HTTPStatus.BAD_REQUEST
        body['artist_id'] = artist_id
        try:
            DBHelper.run_query(AlbumArtistRelations.post_single_album_artist_relation_query(body))
            return { "msg" : "Creating contribution of album operation successful." }, HTTPStatus.OK
        except:
            return { "msg" : "Creating contribution of album operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class ArtistSongsResource(Resource):

    def get(self, artist_id):
        return DBHelper.run_query(ArtistSongRelations.get_artist_song_relation_query_by_artist_id_all(artist_id)), HTTPStatus.OK

    def post(self, artist_id):
        body = request.get_json(force=True)

        DBHelper.run_query(Songs.post_single_song_query(body))
        id = DBHelper.run_query(Generals.get_last_insert_id("songs"))[0]['max(id)']

        artist_song_relation = {}
        artist_song_relation['artist_id'] = artist_id
        artist_song_relation['song_id'] = id
        artist_song_relation['is_creator'] = 1

        DBHelper.run_query(ArtistSongRelations.post_single_artist_song_relation_query_with_owner(artist_song_relation))

        album_song_relation = {}
        album_song_relation['album_id'] = body['album_id']
        album_song_relation['song_id'] = id

        DBHelper.run_query(AlbumSongRelations.post_album_song_relation_query(album_song_relation))

        for artist in body['coworkers']:
            artist_song_relation = {}
            artist_song_relation['artist_id'] = artist
            artist_song_relation['song_id'] = id
            DBHelper.run_query(ArtistSongRelations.post_single_artist_song_relation_query(artist_song_relation))

        return { "msg" : "Creating artist song operation successful." }, HTTPStatus.CREATED

    def delete(self, artist_id):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Songs.delete_single_song_query(body['song_id']))

            album_song_relation = {}
            album_song_relation['song_id'] = body['song_id']
            album_song_relation['album_id'] = body['album_id']

            DBHelper.run_query(ArtistSongRelations.delete_artist_song_relation_query_by_song_id(body['song_id']))
            DBHelper.run_query(AlbumSongRelations.delete_album_song_relation_query(album_song_relation))
            return { "msg" : "Deleting artist song operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting artist song operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class ArtistPopularSongsResource(Resource):

    def get(self, artist_id):
        return DBHelper.run_query(ArtistSongRelations.get_popular_song_of_an_artist_query_by_artist_id(artist_id)), HTTPStatus.OK

class ArtistsRanksResource(Resource):

    def post(self):
        body = request.get_json(force=True)
        if body['type'] == 'active':
            artists = DBHelper.run_query(Artists.get_active_artists_query())
        if body['type'] == 'all':
            artists = DBHelper.run_query(Artists.get_artists_query())
        artist_ranks = []
        for artist in artists:
            rank_info = {}
            artist_songs = DBHelper.run_query(ArtistSongRelations.get_artist_song_relation_query_by_artist_id_all(artist['id']))
            total_likes = 0
            for song in artist_songs:
                total_likes = total_likes + song['likes']
            if artist['surname'] is None:
                rank_info['artist_name'] = artist['name']
            else:
                rank_info['artist_name'] = artist['name'] + " " + artist['surname']
            rank_info['total_likes'] = total_likes
            artist_ranks.append(rank_info)
        sorted_ranks = sorted(artist_ranks, key=lambda x: x['total_likes'], reverse=True)
        return sorted_ranks, HTTPStatus.OK

class ArtistsCoworkedOnASongResource(Resource):

    def get(self, song_id):
        try:
            DBHelper.run_query(StoredProcedures.get_coworkers_by_stored())
        except Exception:
            pass

        return DBHelper.run_query(ArtistSongRelations.get_artist_song_relation_query_by_song_id(song_id)), HTTPStatus.OK
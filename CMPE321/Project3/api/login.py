import json
from http import HTTPStatus

from flask import request
from flask_restful import Resource

from db.helper import DBHelper
from db.utils import Listeners, Artists

class LoginArtistResource(Resource):

    def get(self):
        return DBHelper.run_query(Artists.get_artists_query()), HTTPStatus.OK

    def post(self):
        body = request.get_json(force=True)

        artists = DBHelper.run_query(Artists.get_artists_query())
        for artist in artists:
            if artist['name'] == body['name']:
                if artist['surname'] == body['surname']:
                    return { "msg" : "Attempted to create duplicate artist." }, HTTPStatus.BAD_REQUEST

        try:
            DBHelper.run_query(Artists.post_single_artist_query(body))
            return { "msg" : "Creating artist operation successful." }, HTTPStatus.CREATED
        except Exception:
            return { "msg" : "Creating artist operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self):
        body = request.get_json(force=True)

        try:
            if type(body['id']) == type([]):
                DBHelper.run_query(Artists.delete_multiple_artist_query(body['id']))
            else:
                DBHelper.run_query(Artists.delete_single_artist_query(body['id']))
            return { "msg" : "Deleting artist operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting artist operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class LoginListenerResource(Resource):

    def get(self):
        return DBHelper.run_query(Listeners.get_listeners_query()), HTTPStatus.OK
    
    def post(self):
        body = request.get_json(force=True)

        try:
            DBHelper.run_query(Listeners.post_single_listener_query(body))
            return { "msg" : "Creating listener operation successful." }, HTTPStatus.CREATED
        except Exception:
            return { "msg" : "Creating listener operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

    def delete(self):
        body = request.get_json(force=True)

        try:
            if type(body['id']) == type([]):
                DBHelper.run_query(Listeners.delete_multiple_listener_query(body['id']))
            else:
                DBHelper.run_query(Listeners.delete_single_listener_query(body['id']))
            return { "msg" : "Deleting listener operation successful." }, HTTPStatus.OK
        except Exception:
            return { "msg" : "Deleting listener operation FAILED!!!" }, HTTPStatus.BAD_REQUEST

class LoginResource(Resource):

    def post(self):
        body = json.loads(request.get_json(force=True))

        if body['log-type'] == 'artist':
            validation = DBHelper.run_query(Artists.get_artist_query_by_name_by_surname(body))
            if len(validation) > 0:
                return { "msg" : "Login Successful." }, HTTPStatus.OK
            return { "msg" : "Login Failed." }, HTTPStatus.UNAUTHORIZED
        if body['log-type'] == 'listener':
            validation = DBHelper.run_query(Listeners.get_listener_query_by_username_by_email(body))
            if len(validation) > 0:
                return { "msg" : "Login Successful." }, HTTPStatus.OK
            return { "msg" : "Login Failed." }, HTTPStatus.UNAUTHORIZED
        return { "msg" : "Invalid request" }, HTTPStatus.BAD_REQUEST

class ArtistResource(Resource):

    def post(self):
        body = request.get_json(force=True)
        credentials = {}
        credentials['name'] = body['name']
        if set(body.keys()).issuperset(set("surname")):
            credentials['surname'] = body['surname']
            artist = DBHelper.run_query(Artists.get_artist_query_by_name_by_surname(credentials))
        else:
            artist = DBHelper.run_query(Artists.get_artist_query_by_name(body['name']))
        if len(artist) > 0:
            return artist[0]['id'], HTTPStatus.OK
        return { "msg" : "Artist not found." }, HTTPStatus.BAD_REQUEST
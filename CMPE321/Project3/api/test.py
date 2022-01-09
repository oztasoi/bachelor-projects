import json
from http import HTTPStatus

from flask_restful import Resource

class TestResource(Resource):

    def get(self):
        return { "msg" : "Hello, it seems I am WORKING!!!" }, HTTPStatus.OK
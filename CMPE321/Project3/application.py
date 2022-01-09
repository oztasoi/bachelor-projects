from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.test import TestResource
from api.login import LoginArtistResource, LoginListenerResource, LoginResource, ArtistResource
from api.albums import AlbumsResource, AlbumLikesResource, AlbumSongsResource
from api.songs import SongsResource, SongLikesResource, SongSearchByGenreResource, SongSearchByKeywordResource
from api.listeners import ListenerSongsResource, ListenerAlbumsResource
from api.artists import ArtistAlbumsResource, ArtistSongsResource, ArtistPopularSongsResource, ArtistsRanksResource, ArtistsCoworkedOnASongResource

from db.helper import DBHelper

application = Flask(__name__)
cors = CORS(application)
application.config.from_object('config.Config')

DBHelper.init_app(application)

api = Api(application)
api.add_resource(TestResource, "/test")
api.add_resource(LoginResource, "/login")
api.add_resource(ArtistResource, "/artists")
api.add_resource(LoginArtistResource, "/login-artist")
api.add_resource(LoginListenerResource, "/login-listener")
api.add_resource(AlbumsResource, "/albums")
api.add_resource(SongsResource, "/songs")
api.add_resource(AlbumSongsResource, "/albums/songs/<int:album_id>")
api.add_resource(SongLikesResource, "/songs/<int:song_id>")
api.add_resource(AlbumLikesResource, "/albums/<int:album_id>")
api.add_resource(ListenerSongsResource, "/listeners/songs/<int:listener_id>")
api.add_resource(ListenerAlbumsResource, "/listeners/albums/<int:listener_id>")
api.add_resource(ArtistSongsResource, "/artists/songs/<int:artist_id>")
api.add_resource(ArtistAlbumsResource, "/artists/albums/<int:artist_id>")
api.add_resource(ArtistPopularSongsResource, "/popular/artists/<int:artist_id>")
api.add_resource(ArtistsRanksResource, "/rankings")
api.add_resource(SongSearchByGenreResource, "/search-by-genre/<string:genre>")
api.add_resource(SongSearchByKeywordResource, "/search-by-keyword/<string:keyword>")
api.add_resource(ArtistsCoworkedOnASongResource, "/coworked/<int:song_id>")

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5001)
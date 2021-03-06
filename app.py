from base import Movies, db
from flask import Flask
from flask_restful import Resource, reqparse, Api

# Init flask object

app = Flask(__name__)

# Init Api object

api = Api(app)

# Set location for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

# Configurations
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
app.app_context().push()
db.create_all()


# Class to create get, post, put & delete methods

class Movies_List(Resource):

    # Instantiating a parser object to hold data from message payload
    parser = reqparse.RequestParser()
    parser.add_argument('director', type=str, required=False,
                        help='Director of the movie')
    parser.add_argument('genre', type=str, required=False,
                        help='Genre of the movie')
    parser.add_argument('collection', type=int, required=True,
                        help='Gross collection of the movie')

    # Get method
    def get(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            return item.json()
        return {'Message': 'Movie is not found'}

    # Post method
    def post(self, movie):
        if Movies.find_by_title(movie):
            return {'Message': 'Movie with the title {} already exists'.format(movie)}
        args = Movies_List.parser.parse_args()
        item = Movies(movie, args['director'],
                      args['genre'], args['collection'])
        item.save_to()
        return item.json()

    # Put method
    def put(self, movie):
        args = Movies_List.parser.parse_args()
        item = Movies.find_by_title(movie)
        if item:
            item.collection = args['collection']
            item.save_to()
            return {'Movie': item.json()}
        item = Movies(movie, args['director'],
                      args['genre'], args['collection'])
        item.save_to()
        return item.json()

    # Delete method
    def delete(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from records'.format(movie)}
        return {'Message': '{} is already not on the list'.format()}

# Create a class to get all movies from database


class All_Movies(Resource):

    # Get method
    def get(self):
        return {'Movies': list(map(lambda x: x.json(), Movies.query.all()))}


# Adding URIs to api
api.add_resource(All_Movies, '/')
api.add_resource(Movies_List, '/<string:movie>')

if __name__ == '__main__':
    app.run()

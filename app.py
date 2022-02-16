# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from schemas import MovieSchema, GenreSchema, DirectorSchema

app = Flask(__name__)

api = Api(app)
movie_ns = api.namespace("movies")
genre_ns = api.namespace("genres")
director_ns = api.namespace("directors")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):

        movies_schema = MovieSchema(many=True)
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")

        movies = []

        if director_id and genre_id:
            movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies = Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id).all()
        else:
            movies = Movie.query.all()

        if movies:
            return movies_schema.dump(movies), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201

@movie_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        if movie:
            return MovieSchema().dump(movie), 200
        else:
            return "", 404

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json
        # movie.text = req_json.get("text")
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        # with db.session.begin():
        db.session.add(movie)
        db.session.commit()

        return "", 201

    # title = db.Column(db.String(255))
    # description = db.Column(db.String(255))
    # trailer = db.Column(db.String(255))
    # year = db.Column(db.Integer)
    # rating = db.Column(db.Float)
    # genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    # genre = db.relationship("Genre")
    # director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # director = db.relationship("Director")

    def patch(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "description" in req_json:
            movie.trailer = req_json.get("trailer")
        if "description" in req_json:
            movie.year = req_json.get("year")
        if "description" in req_json:
            movie.rating = req_json.get("rating")
        if "description" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "description" in req_json:
            movie.director_id = req_json.get("director_id")
        # if "text" in req_json:
        #     note.text = req_json.get("text")
        # if "author" in req_json:
        #     note.author = req_json.get("author")
        # with db.session.begin():
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if not movie:
            return "", 404
        # with db.session.begin():
        db.session.delete(movie)
        db.session.commit()
        return "", 204



@genre_ns.route("/")
class GenresView(Resource):
    def get(self):

        genres_schema = GenreSchema(many=True)

        genres = []

        # if director_id and genre_id:
        #     movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        # elif director_id:
        #     movies = Movie.query.filter_by(director_id=director_id).all()
        # elif genre_id:
        #     movies = Movie.query.filter_by(genre_id=genre_id).all()
        # else:
        genres = Genre.query.all()

        if genres:
            return genres_schema.dump(genres), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201

@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid):
        genre = Genre.query.get(gid)
        if genre:
            return GenreSchema().dump(genre), 200
        else:
            return "", 404

    def put(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()

        return "", 201

    # title = db.Column(db.String(255))
    # description = db.Column(db.String(255))
    # trailer = db.Column(db.String(255))
    # year = db.Column(db.Integer)
    # rating = db.Column(db.Float)
    # genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    # genre = db.relationship("Genre")
    # director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # director = db.relationship("Director")

    def patch(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        req_json = request.json

        if "name" in req_json:
            genre.name = req_json.get("name")
        # if "title" in req_json:
        #     movie.title = req_json.get("title")
        # if "description" in req_json:
        #     movie.description = req_json.get("description")
        # if "description" in req_json:
        #     movie.trailer = req_json.get("trailer")
        # if "description" in req_json:
        #     movie.year = req_json.get("year")
        # if "description" in req_json:
        #     movie.rating = req_json.get("rating")
        # if "description" in req_json:
        #     movie.genre_id = req_json.get("genre_id")
        # if "description" in req_json:
        #     movie.director_id = req_json.get("director_id")
        # if "text" in req_json:
        #     note.text = req_json.get("text")
        # if "author" in req_json:
        #     note.author = req_json.get("author")
        # with db.session.begin():
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if not genre:
            return "", 404
        # with db.session.begin():
        db.session.delete(genre)
        db.session.commit()
        return "", 204



@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):

        directors_schema = DirectorSchema(many=True)

        directors = []

        # if director_id and genre_id:
        #     movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        # elif director_id:
        #     movies = Movie.query.filter_by(director_id=director_id).all()
        # elif genre_id:
        #     movies = Movie.query.filter_by(genre_id=genre_id).all()
        # else:
        directors = Director.query.all()

        if directors:
            return directors_schema.dump(directors), 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201

@director_ns.route("/<int:did>")
class GenreView(Resource):
    def get(self, did):
        director = Director.query.get(did)
        if director:
            return GenreSchema().dump(director), 200
        else:
            return "", 404

    def put(self, did: int):
        director = Director.query.get(did)
        if not director:
            return "", 404
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()

        return "", 201

    # title = db.Column(db.String(255))
    # description = db.Column(db.String(255))
    # trailer = db.Column(db.String(255))
    # year = db.Column(db.Integer)
    # rating = db.Column(db.Float)
    # genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    # genre = db.relationship("Genre")
    # director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # director = db.relationship("Director")

    def patch(self, did: int):
        director = Director.query.get(did)
        if not director:
            return "", 404
        req_json = request.json

        if "name" in req_json:
            director.name = req_json.get("name")
        # if "title" in req_json:
        #     movie.title = req_json.get("title")
        # if "description" in req_json:
        #     movie.description = req_json.get("description")
        # if "description" in req_json:
        #     movie.trailer = req_json.get("trailer")
        # if "description" in req_json:
        #     movie.year = req_json.get("year")
        # if "description" in req_json:
        #     movie.rating = req_json.get("rating")
        # if "description" in req_json:
        #     movie.genre_id = req_json.get("genre_id")
        # if "description" in req_json:
        #     movie.director_id = req_json.get("director_id")
        # if "text" in req_json:
        #     note.text = req_json.get("text")
        # if "author" in req_json:
        #     note.author = req_json.get("author")
        # with db.session.begin():
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, did: int):
        director = Director.query.get(did)
        if not director:
            return "", 404
        # with db.session.begin():
        db.session.delete(director)
        db.session.commit()
        return "", 204



if __name__ == '__main__':
    app.run(debug=True)

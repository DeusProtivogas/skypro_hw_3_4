# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from schemas import MovieSchema

app = Flask(__name__)

api = Api(app)
movie_ns = api.namespace("movies")

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



if __name__ == '__main__':
    app.run(debug=True)

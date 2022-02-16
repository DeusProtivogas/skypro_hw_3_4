from marshmallow import fields, Schema


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
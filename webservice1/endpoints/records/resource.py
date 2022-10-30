from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Record
from app import db

record_fields = {
    'movie': fields.String,
    'actor': fields.String,
    'country': fields.String,
    'order': fields.String,
    'date': fields.String
}

records_fields = {
    'count': fields.Integer,
    'records': fields.List(fields.Nested(record_fields)),
}

# define parameter format
parser = reqparse.RequestParser()
parser.add_argument("movie", type=str,
                    help="Please check the movie name", location=['json'])
parser.add_argument("actor",
                    type=str, help="Please check the actor", location=['json'])
parser.add_argument("country",
                    type=str, help="Please check the country", location=['json'])
parser.add_argument("order", type=str,
                    help="Please check the popularity", location=['json'])

parser.add_argument('date', )


# Search
#   show, post search item and lets you delete them
class RecordResource(Resource):
    def get(self, record_id=None):
        if record_id:
            record = Record.query.filter_by(id=record_id).first()
            return record
        else:
            record = Record.query.all()
            print(record)

            return marshal({
                'count': len(record),
                'records': [marshal(t, record_fields) for t in record]
            }, records_fields)

    @marshal_with(record_fields)
    def delete(self, record_id=None):
        record = Record.query.filter_by(id=record_id).first()
        db.session.delete(record)
        db.session.commit()
        return 'delete success', 204

    @marshal_with(record_fields)
    def post(self):
        args = parser.parse_args()
        record = Record(**args)
        db.session.add(record)
        db.session.commit()
        return record

    @marshal_with(record_fields)
    def put(self, record_id):
        record = Record.query.get(record_id)

        if 'movie' in request.json:
            record.movie = request.json['movie']

        if 'description' in request.json:
            record.actor = request.json['actor']

        db.session.commit()
        return record

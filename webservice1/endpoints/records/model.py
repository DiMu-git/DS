from app import db
import datetime


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String(20))
    actor = db.Column(db.String(20))
    country = db.Column(db.String(10))
    order = db.Column(db.String(10))
    date = db.Column(db.Date, default=datetime.datetime.now())

    def __repr__(self):
        return 'Id: {}, movie: {}'.format(self.id, self.movie)

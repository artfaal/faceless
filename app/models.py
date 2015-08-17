from app import db

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index = True, unique = True)
    slug = db.Column(db.String(32), index = True, unique = True)
    position = db.Column(db.Integer)

    def __repr__(self):
        return '<Tovar %r>' % (self.name)
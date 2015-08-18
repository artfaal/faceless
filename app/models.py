from app import db

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index = True, unique = True)
    slug = db.Column(db.String(32), unique = True)
    position = db.Column(db.Integer)
    meta_keywords = db.Column(db.String(200), index = True)
    meta_description = db.Column(db.String(200), index = True)
    body = db.Column(db.String, index = True)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Tovar %r>' % (self.name)


class TovarImg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(32), unique = True)
    alt = db.Column(db.String(64))
    pid = db.Column(db.Integer, db.ForeignKey('tovar.id'))


class TovarDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(32), unique = True)
    alt = db.Column(db.String(64))
    pid = db.Column(db.Integer, db.ForeignKey('tovar.id'))


class TovarVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64))
    alt = db.Column(db.String(64))
    pid = db.Column(db.Integer, db.ForeignKey('tovar.id'))


class MainCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index = True, unique = True)
    slug = db.Column(db.String(32), unique = True)
    meta_keywords = db.Column(db.String(200), index = True)
    meta_description = db.Column(db.String(200), index = True)
    mini_description = db.Column(db.String(500), index = True)
    body = db.Column(db.String, index = True)
    image = db.Column(db.String(200), unique = True)
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)



class ChildCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index = True, unique = True)
    slug = db.Column(db.String(32), unique = True)
    meta_keywords = db.Column(db.String(200), index = True)
    meta_description = db.Column(db.String(200), index = True)
    mini_description = db.Column(db.String(500), index = True)
    body = db.Column(db.String, index = True)
    image = db.Column(db.String(200), unique = True)
    parent = db.Column(db.Integer, db.ForeignKey('maincat.id'))
    position = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
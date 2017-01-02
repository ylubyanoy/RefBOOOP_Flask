from ref_prj import db


class Usersdb(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    userpass = db.Column(db.String(50))
    isadmin = db.Column(db.Integer)
    otraslid = db.Column(db.Integer)
    isbooop = db.Column(db.Integer)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

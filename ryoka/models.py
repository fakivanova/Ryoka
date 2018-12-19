from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import inspect
from . import db, login_manager, udb_sessions, udbmodels

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    rank = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def session(self):
        if self.id is None:
            return None
        return udb_sessions[self.id]

    @property
    def is_udb_initialized(self):
        if hasattr(self, '_is_udb_initialized'):
            return self._is_udb_initialized
        if self.id is None:
            return False
        session = udb_sessions[self.id]
        required_tables = set(udbmodels.Base.metadata.tables.keys())
        existed_tables = set(inspect(session.get_bind()).get_table_names())
        self._is_udb_initialized = (required_tables == existed_tables)
        return self._is_udb_initialized


    @property
    def number_of_diseases(self):
        if self.id is None or not self.is_udb_initialized:
            return None
        session = udb_sessions[self.id]
        return session.query(udbmodels.Diseas).count()

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    charactersFav = db.relationship("Character", secondary="character_favs", lazy='subquery', backref=db.backref('users', lazy=True))
    locationsFav = db.relationship("Location", secondary="location_favs", lazy='subquery', backref=db.backref('users', lazy=True))
    episodesFav = db.relationship("Episode", secondary="episode_favs",lazy='subquery', backref=db.backref('users', lazy=True))
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
          #  "character_favs": [character.serialize() for character in self.character],
           # "location_favs": [location.serialize() for location in self.location],
           # "episode_favs": [episode.serialize() for episode in self.episode]
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    species = db.Column(db.String(250),unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "gender": self.gender,
            "alive": self.alive,
            "species": self.species
        }

character_favs = db.Table('character_favs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), unique=True, nullable=False)
    location_type = db.Column(db.String(250), unique=False, nullable=False)
    dimension = db.Column(db.String(250), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "location_name": self.location_name,
            "location_type": self.location_type,
            "dimension": self.dimension,
        }    

location_favs = db.Table('location_favs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'), primary_key=True)
)

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_name = db.Column(db.String(120), unique=True, nullable=False)
    air_date = db.Column(db.String(250), unique=False, nullable=False)
    episode = db.Column(db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "episode_name": self.episode_name,
            "air_date": self.air_date,
            "episode": self.episode,
        }  

episode_favs = db.Table('episode_favs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('episode_id', db.Integer, db.ForeignKey('episode.id'), primary_key=True)
)

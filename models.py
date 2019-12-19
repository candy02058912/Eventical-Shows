from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    shows = db.relationship(
        'Show', back_populates="venue", cascade='all')

    def get_upcoming_shows(self):
        now = datetime.now()
        return [show for show in self.shows if show.start_time >= now]

    def get_past_shows(self):
        now = datetime.now()
        return [show for show in self.shows if show.start_time < now]

    def serialize(self):
        upcoming_shows = self.get_upcoming_shows()
        upcoming_shows_count = len(upcoming_shows)
        past_shows = self.get_past_shows()
        past_shows_count = len(past_shows)
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres.split(','),
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'website': self.website,
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': upcoming_shows_count,
            'past_shows': past_shows,
            'past_shows_count': past_shows_count,
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    shows = db.relationship('Show', back_populates="artist", cascade='all')

    def get_upcoming_shows(self):
        now = datetime.now()
        return [show for show in self.shows if show.start_time >= now]

    def get_past_shows(self):
        now = datetime.now()
        return [show for show in self.shows if show.start_time < now]

    def serialize(self):
        upcoming_shows = self.get_upcoming_shows()
        upcoming_shows_count = len(upcoming_shows)
        past_shows = self.get_past_shows()
        past_shows_count = len(past_shows)
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres.split(','),
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'website': self.website,
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': upcoming_shows_count,
            'past_shows': past_shows,
            'past_shows_count': past_shows_count,
        }


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue = db.relationship('Venue', back_populates='shows', lazy=True)
    artist = db.relationship('Artist', back_populates='shows', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'start_time': self.start_time,
            'venue_id': self.venue_id,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'venue_name': self.venue.name,
            'artist_image_link': self.artist.image_link,
            'venue_image_link': self.venue.image_link
        }

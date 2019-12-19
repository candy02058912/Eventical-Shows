from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL
from enums import GenreEnum, StateEnum


def ValidateGenre(form, field):
    if len(set(field.data) - set([c.value for c in GenreEnum])) != 0:
        raise ValidationError('Fields available are %s' %
                              ([c for c in GenreEnum]))


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), ValidateGenre],
        choices=GenreEnum.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    seeking_talent = BooleanField('seeking_talent')


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices()
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), ValidateGenre],
        choices=GenreEnum.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    seeking_venue = BooleanField('seeking_venue')

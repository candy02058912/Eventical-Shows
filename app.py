#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler, INFO
from forms import *
from models import db, Venue, Artist, Show
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(date, format='medium'):
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en_US')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.order_by(Venue.state, Venue.city).all()
    data = {}
    cities = []

    for venue in venues:
        if (venue.city, venue.state) not in cities:
            data[(venue.city, venue.state)] = {
                'city': venue.city,
                'state': venue.state,
                'venues': [venue.serialize()]
            }
            cities.append((venue.city, venue.state))
        else:
            data[(venue.city, venue.state)]['venues'].append(venue.serialize())
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    if search_term:
        results = Venue.query.filter(
            Venue.name.ilike('%{}%'.format(search_term))).all()
        data = [result.serialize() for result in results]
        response = {
            'count': len(results),
            'data': data
        }
    else:
        response = {
            'count': 0,
            'data': []
        }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue:
        data = venue.serialize()
        return render_template('pages/show_venue.html', venue=data)
    abort(404)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if not form.validate():
        flash(form.errors)
        return render_template('forms/new_venue.html', form=form)
    error=False
    try:
        venue=Venue()
        venue.name=request.form['name']
        venue.city=request.form['city']
        venue.state=request.form['state']
        venue.address=request.form['address']
        venue.phone=request.form['phone']
        venue.genres=','.join(request.form.getlist('genres'))
        venue.facebook_link=request.form['facebook_link']
        venue.image_link=request.form['image_link']
        venue.website=request.form['website']
        venue.seeking_talent=request.form.get('seeking_talent') is not None
        venue.seeking_description=request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be listed.')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods = ['DELETE'])
def delete_venue(venue_id):
    error=False
    try:
        venue=Venue.query.get(venue_id)
        name=venue.name
        db.session.delete(venue)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' +
                  name + ' could not be deleted.')
        else:
            flash('Venue ' + name +
                  ' was successfully deleted!')
        return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data=Artist.query.all()
    return render_template('pages/artists.html', artists = data)


@app.route('/artists/search', methods = ['POST'])
def search_artists():
    search_term=request.form.get('search_term')
    if search_term:
        results=Artist.query.filter(
            Artist.name.ilike('%{}%'.format(search_term))).all()
        data = [result.serialize() for result in results]
        response = {
            'count': len(results),
            'data': data
        }
    else:
        response = {
            'count': 0,
            'data': []
        }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    data = artist.serialize()
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' +
                  artist.name + ' could not be deleted.')
        else:
            flash('Artist ' + artist.name +
                  ' was successfully deleted!')
        return render_template('pages/home.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        artist = Artist()
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = ','.join(request.form.getlist('genres'))
        artist.facebook_link = request.form['facebook_link']
        artist.image_link = request.form['image_link']
        artist.seeking_venue = request.form.get('seeking_venue') is not None
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' +
                  request.form['name'] + ' could not be edited.')
        else:
            flash('Artist ' + request.form['name'] +
                  ' was successfully edited!')
            return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    try:
        venue = Venue()
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = ','.join(request.form.getlist('genres'))
        venue.facebook_link = request.form['facebook_link']
        venue.image_link = request.form['image_link']
        venue.seeking_talent = request.form.get('seeking_talent') is not None
        venue.seeking_description = request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be edited.')
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully edited!')
            return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if not form.validate():
        flash(form.errors)
        return render_template('forms/new_artist.html', form=form)
    error = False
    try:
        artist = Artist()
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = ','.join(request.form.getlist('genres'))
        artist.facebook_link = request.form['facebook_link']
        artist.website = request.form['website']
        artist.image_link = request.form['image_link']
        artist.seeking_venue = request.form.get('seeking_venue') is not None
        artist.seeking_description = request.form['seeking_description']
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' +
                  request.form['name'] + ' could not be listed.')
        else:
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = [show.serialize() for show in shows]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        show = Show()
        show.artist_id = request.form['artist_id']
        show.venue_id = request.form['venue_id']
        show.start_time = request.form['start_time']
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('Show was successfully listed!')
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import ARRAY, String
from forms import *
from flask_migrate import Migrate
import sys;
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(ARRAY(String))
    shows = db.relationship('Show', backref='venue', lazy='dynamic')

    def __repr__(self):
        return f'<Venue ID: {self.id}, name: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(ARRAY(String))
    shows = db.relationship('Show', backref='artist')

    def __repr__(self):
      return f'<Artist ID: {self.id}, name: {self.name}>'
  
class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer,  db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show ID: {self.id}>'


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  venues = Venue.query.all()
  now = datetime.now()

  cities_states = set()
  for venue in venues:
    cities_states.add((venue.city, venue.state))
  list_cities_states = list(cities_states)

  response = []
  for item in list_cities_states:
    list_venues = []
    for venue in venues:
      if(venue.city == item[0]) and (venue.state == item[1]):
        number_of_upcomming = 0
        shows = venue.shows
        for show in shows:
          if(show.start_time > now):
            number_of_upcomming = number_of_upcomming + 1

        list_venues.append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": number_of_upcomming
        })

    response.append({
        "city": item[0],
        "state": item[1],
        "venues": list_venues
    })
    print(response)
  return render_template('pages/venues.html', areas=response)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_query = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_query}%')).all()
  current_time = datetime.now()

  rs = []
  for venue in venues:
    shows = Show.query.filter_by(venue_id=venue.id).all()
    num_upcoming_shows = 0
    for show in shows:
      if show.start_time > current_time:
        num_upcoming_shows = num_upcoming_shows + 1
    rs.append({
      "id" : venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_shows
    })

  response={
    "count": len(venues),
    "data": rs
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)

  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in venue.shows:
    if(show.start_time > current_time) :
      upcoming_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })
    else:
      past_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })

  response={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_venue.html', venue=response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  print(request.form)
  try:
    newVenue = Venue(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      address=request.form['address'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      website=request.form['website'] if 'website' in request.form else '',
      facebook_link=request.form['facebook_link'] if 'facebook_link' in request.form else '',
      image_link=request.form['image_link'] if 'image_link' in request.form else '',
      seeking_talent=True if 'seeking_talent' in request.form and request.form['seeking_talent'] == 'y' else False ,
      seeking_description=request.form['seeking_description'] if 'seeking_description' in request.form else '',
    )
    db.session.add(newVenue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return None

#  Update
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = db.session.get(Venue, venue_id)
  form = VenueForm()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = db.session.get(Venue, venue_id)

    venue.name = request.form['name']
    venue.genres=request.form.getlist('genres')
    venue.address=request.form['address']
    venue.city=request.form['city']
    venue.state=request.form['state']
    venue.phone=request.form['phone']
    venue.website=request.form['website'] if 'website' in request.form else ''
    venue.facebook_link=request.form['facebook_link'] if 'facebook_link' in request.form else ''
    venue.image_link=request.form['image_link'] if 'image_link' in request.form else ''
    venue.seeking_talent = True if 'seeking_talent' in request.form and request.form['seeking_talent'] == 'y' else False
    venue.seeking_description=request.form['seeking_description'] if 'seeking_description' in request.form else ''

    db.session.commit()
  except: 
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_query = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_query}%')).all()
  current_time = datetime.now()

  rs = []
  for artist in artists:
    shows = Show.query.filter_by(artist_id=artist.id).all()
    num_upcoming_shows = 0
    for show in shows:
      if show.start_time > current_time:
        num_upcoming_shows = num_upcoming_shows + 1
    rs.append({
      "id" : artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows
    })

  response={
    "count": len(artists),
    "data": rs
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)

  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in artist.shows:
    if(show.start_time > current_time) :
      upcoming_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })
    else:
      past_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      })
  
  response={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=response)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.get(Artist, artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = db.session.get(Artist, artist_id)

    artist.name = request.form['name']
    artist.genres=request.form.getlist('genres')
    artist.city=request.form['city']
    artist.state=request.form['state']
    artist.phone=request.form['phone']
    artist.website=request.form['website'] if 'website' in request.form else ''
    artist.facebook_link=request.form['facebook_link'] if 'facebook_link' in request.form else ''
    artist.image_link=request.form['image_link'] if 'image_link' in request.form else ''
    artist.seeking_venue = True if 'seeking_venue' in request.form and request.form['seeking_venue'] == 'y' else False
    artist.seeking_description=request.form['seeking_description'] if 'seeking_description' in request.form else ''

    db.session.commit()
  except: 
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    newArtist = Artist(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      website=request.form['website'] if 'website' in request.form else '',
      facebook_link=request.form['facebook_link'] if 'facebook_link' in request.form else '',
      image_link=request.form['image_link'] if 'image_link' in request.form else '',
      seeking_venue=True if 'seeking_venue' in request.form and request.form['seeking_venue'] == 'Yes' else False,
      seeking_description=request.form['seeking_description'] if 'seeking_description' in request.form else ''
    )
    db.session.add(newArtist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()

  response = []
  for show in shows:
    response.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=response)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
      new_show = Show(
        start_time=request.form['start_time'], 
        artist_id=request.form['artist_id'], 
        venue_id=request.form['venue_id']
      )
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
  finally:
      db.session.close()
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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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


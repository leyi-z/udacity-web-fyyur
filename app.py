#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import logging
import sys

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#import models
from models import db
from models import *



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')



#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data_venues = db.session.query(Venue).all()
  data_shows = db.session.query(Show).all()
  data_cities = db.session.query(Venue.city, Venue.state).all()
  data_cities = list(set(data_cities))
  data_cities.sort(key=lambda i: i.state)
  data_venues.sort(reverse=True, key=lambda venue: sum(1 for show in data_shows if show.venue_id==venue.id))
  return render_template('pages/venues.html', 
      data_venues = data_venues,
      data_cities = data_cities
  )


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_input = request.form.get('search_term')
    venues = db.session.query(Venue).all()
    venue_results = [v for v in venues if search_input.lower() in v.name.lower()]
    results_num = len(venue_results)
    return render_template('pages/search_venues.html',
        venue_results=venue_results,
        search_input=search_input,
        results_num=results_num
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    venue = db.session.query(Venue).filter(Venue.id==venue_id).all()
    data_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
    upcoming_shows = [show for show in data_shows if show.start_time>current_time]
    past_shows = [show for show in data_shows if show.start_time<current_time]
    return render_template('pages/show_venue.html',
        data_shows=data_shows,
        venue=venue[0],
        upcoming_shows=upcoming_shows,
        upcoming_shows_count=len(upcoming_shows),
        past_shows=past_shows,
        past_shows_count=len(past_shows)
    )
    
    

#  ----------------------------------------------------------------    
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create/add', methods=['POST'])
def create_venue_submission():
    error = False
    body = {}
    try:
        new_name = request.get_json()['new_name']
        new_city = request.get_json()['new_city']
        new_state = request.get_json()['new_state']
        new_address = request.get_json()['new_address']
        new_phone = request.get_json()['new_phone']
        new_fblink = request.get_json()['new_fblink']
        new_venue = Venue(
            name=new_name, 
            city=new_city, 
            state=new_state, 
            address=new_address,
            phone=new_phone,
            facebook_link=new_fblink
        )
        db.session.add(new_venue)
        db.session.commit()
        body['id']=new_venue.id
        body['name']=new_venue.name
        body['city']=new_venue.city
        body['state']=new_venue.state
        body['address']=new_venue.address
        body['phone']=new_venue.phone
        body['facebook_link']=new_venue.facebook_link
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + new_name + ' could not be listed.')
        abort(500)
    else:
        flash('Venue ' + new_name + ' was successfully listed!')
        return jsonify(body)


@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        shows = db.session.query(Show).filter(Show.venue_id==venue_id).all()
        for i in shows:
            db.session.delete(i)
        venue = db.session.query(Venue).get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({ 'success': True })

  
 
#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
    data_artists = db.session.query(Artist).all()
    return render_template('pages/artists.html', 
        data_artists = data_artists
    )
    

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_input = request.form.get('search_term')
    artists = db.session.query(Artist).all()
    artist_results = [a for a in artists if search_input.lower() in a.name.lower()]
    results_num = len(artist_results)
    return render_template('pages/search_artists.html',
      artist_results=artist_results,
      search_input=search_input,
      results_num=results_num
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    artist = db.session.query(Artist).filter(Artist.id==artist_id).all()
    data_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).all()
    upcoming_shows = [show for show in data_shows if show.start_time>current_time]
    past_shows = [show for show in data_shows if show.start_time<current_time]
    return render_template('pages/show_artist.html',
        artist=artist[0],
        data_shows=data_shows,
        upcoming_shows=upcoming_shows,
        upcoming_shows_count=len(upcoming_shows),
        past_shows=past_shows,
        past_shows_count=len(past_shows)
    )
    
    

#  ----------------------------------------------------------------    
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = db.session.query(Artist).filter(Artist.id==artist_id).all()
    return render_template('forms/edit_artist.html', 
        form=form, 
        artist=artist[0]
    )


@app.route('/artists/<int:artist_id>/edit/submit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    body = {}
    try:
        new_name = request.get_json()['new_name']
        new_city = request.get_json()['new_city']
        new_state = request.get_json()['new_state']
        new_phone = request.get_json()['new_phone']
        new_fblink = request.get_json()['new_fblink']
        new_artist = Artist(
            name=new_name, 
            city=new_city, 
            state=new_state,
            phone=new_phone,
            facebook_link=new_fblink
        )
        db.session.query(Artist).filter(Artist.id==artist_id).update({
            Artist.name: new_name,
            Artist.city: new_city,
            Artist.state: new_state,
            Artist.phone: new_phone,
            Artist.facebook_link: new_fblink
        })
        db.session.commit()
        body['id']=new_artist.id
        body['name']=new_artist.name
        body['city']=new_artist.city
        body['state']=new_artist.state
        body['phone']=new_artist.phone
        body['facebook_link']=new_artist.facebook_link
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = db.session.query(Venue).filter(Venue.id==venue_id).all()
    return render_template('forms/edit_venue.html', 
        form=form, 
        venue=venue[0]
    )


@app.route('/venues/<int:venue_id>/edit/submit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    body = {}
    try:
        new_name = request.get_json()['new_name']
        new_city = request.get_json()['new_city']
        new_state = request.get_json()['new_state']
        new_phone = request.get_json()['new_phone']
        new_fblink = request.get_json()['new_fblink']
        new_venue = Venue(
            name=new_name, 
            city=new_city, 
            state=new_state,
            phone=new_phone,
            facebook_link=new_fblink
        )
        db.session.query(Venue).filter(Venue.id==venue_id).update({
            Venue.name: new_name,
            Venue.city: new_city,
            Venue.state: new_state,
            Venue.phone: new_phone,
            Venue.facebook_link: new_fblink 
        })
        db.session.commit()
        body['id']=new_venue.id
        body['name']=new_venue.name
        body['city']=new_venue.city
        body['state']=new_venue.state
        body['phone']=new_venue.phone
        body['facebook_link']=new_venue.facebook_link
    except:
       error = True 
       db.session.rollback()
       print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)



#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create/add', methods=['POST'])
def create_artist_submission():
    error = False
    body = {}
    try:
        new_name = request.get_json()['new_name']
        new_city = request.get_json()['new_city']
        new_state = request.get_json()['new_state']
        new_phone = request.get_json()['new_phone']
        new_fblink = request.get_json()['new_fblink']
        new_artist = Artist(
            name=new_name, 
            city=new_city, 
            state=new_state,
            phone=new_phone,
            facebook_link=new_fblink
        )
        db.session.add(new_artist)
        db.session.commit()
        body['id']=new_artist.id
        body['name']=new_artist.name
        body['city']=new_artist.city
        body['state']=new_artist.state
        body['phone']=new_artist.phone
        body['facebook_link']=new_artist.facebook_link
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + new_name + ' could not be listed.')
        abort(500)
    else:
        flash('Artist ' + new_name + ' was successfully listed!')
        return jsonify(body)



#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data_shows = db.session.query(Show).join(Venue, isouter=True).join(Artist, isouter=True).all()
    return render_template('pages/shows.html', 
    data_shows=data_shows
    )
    
    
@app.route('/shows/create', methods=['GET'])
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create/add', methods=['POST'])
def create_show_submission():
    error = False
    body = {}
    try:
        new_artistid = request.get_json()['new_artistid']
        new_venueid = request.get_json()['new_venueid']
        new_time = request.get_json()['new_time']
        new_show = Show(
            artist_id=new_artistid, 
            venue_id=new_venueid, 
            start_time=new_time
        )
        db.session.add(new_show)
        db.session.commit()
        body['id']=new_show.id
        body['artist_id']=new_show.artist_id
        body['venue_id']=new_show.venue_id
        body['start_time']=new_show.start_time
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
        abort(500)
    else:
        flash('Show was successfully listed!')
        return jsonify(body)
    
    
    

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
    db.init_app(app)
        with app.app_context():
            db.create_all()
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

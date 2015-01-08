import os
import json
import requests
from geopy.geocoders import Nominatim

from flask import Flask, render_template, flash

from . import app
from .forms import LocationForm

app.config.from_object(os.environ['APP_SETTINGS'])

WUNDERGROUND_BASE_URL = app.config['WUNDERGROUND_BASE_URL']
WUNDERGROUND_API_KEY = app.config['WUNDERGROUND_API_KEY']

# base urls
CONDITIONS_BASE_URL = '{}{}/conditions/q/'.format(
    WUNDERGROUND_BASE_URL,
    WUNDERGROUND_API_KEY
)
ALMANAC_BASE_URL = '{}{}/almanac/q/'.format(
    WUNDERGROUND_BASE_URL,
    WUNDERGROUND_API_KEY
)


def geocode_location(location):
    "Get lat and lon coordinates for a zip code"
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(location)
        lat = location.latitude
        lon = location.longitude
    except Exception as e:
        print('There was a problem geocoding this address: {}'.format(e))

    return [lat, lon]


def get_current_temp(lat, lon):
    "Get the current temp for a given location"
    r = requests.get('{base}{lat},{lon}'.format(
        base=CONDITIONS_BASE_URL,
        lat=lat,
        lon=lon
    )
    json_string = r.json()
    current_temp = json_string['current_observation']['temp_f']

    return current_temp


def get_record_high(lat, lon):
    "Get the record high in F for a given location"
    r = requests.get('{base}{lat},{lon}'.format(
        base=ALMANAC_BASE_URL,
        lat=lat,
        lon=lon
    )
    json_string = r.json()
    current_temp = json_string['almanac']['temp_high']['record']['F']

def get_record_low(lat, lon):
    "Get the record low in F for a given location"
    r = requests.get('{base}{lat},{lon}'.format(
        base=ALMANAC_BASE_URL,
        lat=lat,
        lon=lon
    )
    json_string = r.json()
    current_temp = json_string['almanac']['temp_low']['record']['F']


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Homepage view
    """
    form = LocationForm()
    if form.validate_on_submit():
        temp_choice = form.temp_choice.data
        location = geocode_location(form.location.data)
        current_temp = get_current_temp(location)
        record_high = get_record_high(location)
        record_low = get_record_low(location)

        if temp_choice == 'hot':
            if current_temp >= record_high:
                flash('It has never been this hot!')
            else:
                flash('It has been this hot before.')
        elif temp_choice == 'cold':
            if current_temp >= record_low:
                flash('It has never been this cold!')
            else:
                flash('It has been this cold before.')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

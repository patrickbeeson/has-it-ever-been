import os
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
    except Exception as e:
        print('There was a problem geocoding this address: {}'.format(e))

    return location


def get_current_temp(lat, lon):
    "Get the current temp for a given location"
    r = requests.get('{base}{lat},{lon}.json'.format(
        base=CONDITIONS_BASE_URL,
        lat=lat,
        lon=lon)
    )
    json_string = r.json()
    current_temp = json_string['current_observation']['temp_f']

    return int(current_temp)


def get_almanac_data(lat, lon):
    "Get the almanac data for a given location"
    r = requests.get('{base}{lat},{lon}.json'.format(
        base=ALMANAC_BASE_URL,
        lat=lat,
        lon=lon)
    )
    json_string = r.json()
    almanac_data = {}
    almanac_data['record_high'] = json_string['almanac']['temp_high']['record']['F']
    almanac_data['record_low'] = json_string['almanac']['temp_low']['record']['F']
    almanac_data['record_high_year'] = json_string['almanac']['temp_high']['recordyear']
    almanac_data['record_low_year'] = json_string['almanac']['temp_low']['recordyear']

    return almanac_data


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Homepage view
    """
    form = LocationForm()
    if form.validate_on_submit():
        temp_choice = form.temp_choice.data
        location = geocode_location(form.location.data)
        lat = location.latitude
        lon = location.longitude
        print(lat, lon)
        current_temp = get_current_temp(lat, lon)
        almanac_data = get_almanac_data(lat, lon)
        record_high = int(almanac_data['record_high'])
        record_low = int(almanac_data['record_low'])
        record_high_year = int(almanac_data['record_high_year'])
        record_low_year = int(almanac_data['record_low_year'])
        temp_diff_high_above = current_temp - record_high
        temp_diff_high_below = record_high - current_temp
        temp_diff_low_above = current_temp - record_low
        temp_diff_low_below = record_low - current_temp

        if temp_choice == 'hot':
            if current_temp >= record_high:
                flash(
                    """It's never been this hot!
                    Currently, it's {} degrees, which is {} degrees above the
                    record of {}, set in {}.""".format(
                    current_temp,
                    temp_diff_high_above,
                    record_high,
                    record_high_year)
                    )
            else:
                flash(
                    """It's been this hot before.
                    Currently, it's {} degrees, which is {} degrees below the
                    record of {}, set in {}.""".format(
                    current_temp,
                    temp_diff_high_below,
                    record_high,
                    record_high_year)
                    )
        else:
            if current_temp <= record_low:
                flash(
                    """It's never been this cold before.
                    Currently, it's {} degrees, which is {} degrees below the
                    record of {}, set in {}.""".format(
                    current_temp,
                    temp_diff_low_below,
                    record_low,
                    record_low_year)
                    )
            else:
                flash(
                    """It's been this cold before.
                    Currently, it's {} degrees, which is {} degrees above the
                    record of {}, set in {}.""".format(
                    current_temp,
                    temp_diff_low_above,
                    record_low,
                    record_low_year)
                    )
        return render_template(
            'index.html',
            form=form,
            current_temp=current_temp,
            record_high=record_high,
            record_low=record_low
        )
    return render_template('index.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

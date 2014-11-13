import os
from flask import Flask
from . import app

app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def home():
    return "Nothing to see here. Move along."

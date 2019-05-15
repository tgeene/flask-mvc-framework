# load flask sub-systems
from flask import render_template

# load application vars
from application import system
from application.config.site import *

# load page
@system.route('/')
def home():
    data = defaults
    data['page'] = {
        'title': 'Home Controller'
    }
    data['meta_description'] = 'Hello, World! Welcome to the Flask MVC Framework.'

    return render_template('home.html', data=data)

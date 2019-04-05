# load flask sub-systems
from flask import render_template, request

# load application vars
from application import system

# load page
@system.route('/')
def home():
    config = {
        'site_title': 'Flask MVC Framework',
        'page_title': 'Home Controller',
        'meta_description': 'Hello, World! Welcome to the Flask MVC Framework.'
    }
    return render_template('home.html', data=config)

# load flask sub-systems
from flask import send_from_directory

# load application vars
from application import system

@system.route('/media/<path:path>')
def load_media(path):
    return send_from_directory('../media', path)
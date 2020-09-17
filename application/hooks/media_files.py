# load flask sub-systems
from flask import send_from_directory

# load application vars
from application import system

# Set Route Path and Function
@system.route('/media/<path:path>')
def load_media(path):
    # Tell system where the media folder is.
    return send_from_directory('../media', path)

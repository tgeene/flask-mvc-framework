# load Flask
import os

# load Flask
from flask import Flask

# load application
from application.config.flask import config
from application.controllers import Controllers

# init Flask
template_dir = os.path.abspath(config['templating']['template_folder'])
static_dir = os.path.abspath(config['templating']['static_folder'])
app = Flask('public', template_folder=template_dir, static_folder=static_dir)
for key in config['flask']:
    app.config[key] = config['flask'][key]

# init Controllers
controllers = Controllers()

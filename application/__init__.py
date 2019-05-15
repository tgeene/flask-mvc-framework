# load Flask
from flask import Flask
system = Flask('application')

# load system config
from application.config.flask import *
for key in flask_config:
    system.config[key] = flask_config[key]

# load hooks
from application.hooks import *

# run controllers
from application.controllers import *

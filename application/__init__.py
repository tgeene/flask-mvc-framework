# load Flask
from flask import Flask
system = Flask('application')

# load system config
from application.config.flask import *
for key in config:
    system.config[key] = config[key]

# load hooks
from application.hooks import *

# run controllers
from application.controllers import *

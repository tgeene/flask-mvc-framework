# load Flask
from flask import Flask

# configure app
system = Flask('application')
system.config['SECRET_KEY'] = b'!T3DxK;L1jJGYf$'
system.config['ENV'] = 'development'
system.config['TESTING'] = True
system.config['DEBUG'] = True

# load Sessions Hook
from application.hooks import *

# run controllers
from application.controllers import *

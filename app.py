# initiate app
from public import app

# load system config
from application.config.flask import config

# run application
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(hostname='127.0.0.1',
               port=80,
               application=app,
               use_reloader=config['flask']['TEMPLATES_AUTO_RELOAD'],
               use_debugger=config['flask']['TESTING'],
               use_evalex=True)

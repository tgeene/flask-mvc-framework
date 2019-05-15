# initiate app
from application import system

# run application
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 5000, system, use_reloader=True, use_debugger=True, use_evalex=True)

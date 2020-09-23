# load flask sub-systems
from flask import render_template
from flask.views import MethodView

# load application vars
from public import app
from application.config.site import defaults


# load page
class Home(MethodView):
    @staticmethod
    def get():
        data = defaults
        data['page'] = {
            'title': 'Home Controller'
        }
        data['meta_description'] = 'Hello, World! Welcome to the Flask MVC Framework.'

        return render_template('home.html', data=data)


app.add_url_rule('/', view_func=Home.as_view('home'))

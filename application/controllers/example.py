# load flask sub-systems
from flask import render_template
from flask.views import MethodView

# load application vars
from public import app
from application.config.site import defaults
from application.models.example import example_model


# load page
class Example(MethodView):
    @staticmethod
    def get():
        data = defaults
        data['page'] = {
            'title': 'Model with DB Connection'
        }
        data['meta_description'] = 'Example of using a model to process database connections.'
        data['users'] = example_model.get_users()

        return render_template('model-with-db-connection.html', data=data)


app.add_url_rule('/model-with-db-connection', view_func=Example.as_view('model_example'))

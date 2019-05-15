# load flask sub-systems
from flask import render_template

# load application vars
from application import system
from application.config.site import *
from application.models.example import example_model

# load page
@system.route('/model-with-db-connection')
def model_with_db():
    data = defaults
    data['page'] = {
        'title': 'Model with DB Connection'
    }
    data['meta_description'] = 'Example of using a model to process database connections.'
    data['users'] = example_model.get_users()

    return render_template('model-with-db-connection.html', data=data)

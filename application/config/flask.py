# Flask Config Variables to be Auto-Loaded
config = {
        'flask': {
                'SECRET_KEY': b'!T3DxK;L1jJGYf$',  # Please change. See Flask for requirements.
                'TESTING': True,
                'TEMPLATES_AUTO_RELOAD': True,
                'SERVER_NAME': 'flask.mvc'
        },
        'templating': {
                'template_folder': 'application/views',
                'static_folder': 'public/assets'
        }
}

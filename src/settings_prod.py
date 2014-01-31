SESSION_COOKIE_NAME = '__session'
ENVIRON_CONFIG = {
    'web_settings' : {
        'ssl_enabled': True
    },
    'webapp2_extras.sessions' : {
        'secret_key': 'some-secret-key-for-prod', #CHANGE ME
        'cookie_name': SESSION_COOKIE_NAME,
        # set the cookie_args accordingly
        #'cookie_args': {'domain': '.directwestbusinesscentre.com'},
    }
}
DEBUG = False
ENVIRONMENT_NAME = "PROD"

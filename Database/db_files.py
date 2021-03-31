import pyrebase
import os

ConfigVars = {
    'apiKey':os.getenv('apiKey'),
    'authDomain':os.getenv('authDomain'),
    'projectId': os.getenv('projectId'),
    'storageBucket':os.getenv('storageBucket'),
    'messagingSenderId':os.getenv('messagingSenderId'),
    'appId':os.getenv('appId'),
    'measurementId':os.getenv('measurementId'),
    'databaseURL':os.getenv('databaseURL')
}

firebase = pyrebase.initialize_app(ConfigVars)
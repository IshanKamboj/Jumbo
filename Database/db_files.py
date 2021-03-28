import pyrebase
import os

firebase = pyrebase.initialize_app(os.getenv('ConfigVars'))
from flask import Flask
import os



app = Flask(__name__)
SECRET_KEY = os.urandom(16)
app.config['SECRET_KEY'] = SECRET_KEY

"""
adding mail feature
"""
# mail server




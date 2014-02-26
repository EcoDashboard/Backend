#!flask/bin/python
from app import app
import os

app.config['SECRET_KEY'] = os.urandom(32)
app.run(debug=True)


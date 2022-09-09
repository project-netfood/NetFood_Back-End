#!/usr/bin/python3
import flask
import socket
import re
import os
import json
import logging
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)

app.config["DEBUG"] = True


@app.route('/fileProd', methods=['GET'])
def get

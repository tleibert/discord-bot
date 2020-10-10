"""
Test flask application
"""

from flask import Flask, json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, Noon World!"

@app.route("/test")
def test_endpoint():
    return json.dumps({"Test Key": "Test Value"})
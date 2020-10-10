"""
Test interacting with the flask application
"""
import requests

resp = requests.get("http://127.0.0.1:5000/test")
jsonn = resp.json()
print(type(jsonn))


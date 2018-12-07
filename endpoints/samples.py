import flask
from flask_restful import Resource
import json
import os

class BBJSON(Resource):
  def get(self):
    with open(os.path.join(
      os.path.dirname(__file__),
      '../samples/api_bulletin_enpoint_example.json'
    )) as file:
      data = json.load(file)

    return data, 200
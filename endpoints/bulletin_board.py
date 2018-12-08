import subprocess
import os
import flask
from flask_restful import Resource, reqparse
import requests

class BulletinBoard(Resource):
  # Gets the contents of the append only bulletin board, throws error
  # throw error if in bad state
  def get(self):

    client_path = os.path.join(os.path.dirname(__file__), "../STAR-Vote/.cabal-sandbox/bin/bbclient")
    client_path = os.path.abspath(client_path)

    command = "{0} 0.0.0.0:8000 read".format(client_path)
    client_read_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    
    bb_json = requests.get('http://0.0.0.0:8000/bb.json')
    pubkey = requests.get('http://0.0.0.0:8000/pubkey.json')
    result = {
      "bb_json": bb_json.json(),
      "pubkey": pubkey.json()
    }

    if client_read_result == 0:
      # THIS SHOULD NOT BE HERE
      return result, 500
    return result, 200

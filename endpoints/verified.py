import subprocess
import os
import flask
from flask_restful import Resource, reqparse
import json


# Contains endpoints to post a user - verified poll tape to
# the underlying append only bulletin board
class Verified(Resource):
  # Post an image, and return the parsed data for verification.
  def post(self):
        # collect message from post request
        data = flask.request.get_json()
        message = data["message"]

        # write message 
        post_file = open("post.txt", "w+")
        post_file.write("1\n" + str(json.dumps(message)))
        post_file.close()

        # generate path to post file
        post_file_path = os.path.join(os.path.dirname(__file__), "../post.txt")
        post_file_path = os.path.abspath(post_file_path)

        # generate path to client executable
        client_path = os.path.join(os.path.dirname(__file__), "../STAR-Vote/.cabal-sandbox/bin/bbclient")
        client_path = os.path.abspath(client_path)

        # execute constructed command
        command = "{0} 0.0.0.0:8000 post < {1}".format(client_path, post_file_path)
        client_post_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        # client_post_result = subprocess.run(command, shell=True)

        successful = client_post_result.returncode == 0
        if successful:
            return "Poll tape posted to bulletin board successfully.", 200
        return "Failed to post poll tape to bulletin board.", 409

from flask import request
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename 
from werkzeug.datastructures import FileStorage
from classes import PollTapeParser, PollTapeTemplate


# Contains endpoints to post images that need to be parsed
# and added to the bulletin board
class Template(Resource):
  # Post an image, and return the parsed data for verification.
  def get(self, district):
    template = PollTapeTemplate()
    template = template.get_template(district)
    if not template:
      return template, 409
    return template, 200


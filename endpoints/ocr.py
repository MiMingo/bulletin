from flask import request
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename 
from werkzeug.datastructures import FileStorage
from classes import PollTapeParser

# Filename parsing from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Contains endpoints to post images that need to be parsed
# and added to the bulletin board
class OCR(Resource):
  # Post an image, and return the parsed data for verification.
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('image', type=FileStorage, location='files', required=True)
    args = parser.parse_args()

    # Check file extension and clean filename
    if allowed_file(args.image.filename) is not True:
      return {'image': '{} type is not supported. must be {}'.format(args.image.filename, ALLOWED_EXTENSIONS)}, 415
    args.image.filename = secure_filename(args.image.filename)
    
    # Initialize a PollTapeParser and return the parsed information.
    ptparser = PollTapeParser(args.image)
    return 'upload success'

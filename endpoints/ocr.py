from flask import request
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename 
from werkzeug.datastructures import FileStorage
from classes import PollTapeParser, PollTapeTemplate

# Filename parsing from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def complete_template(result):
  split_result = result.split('\n')

  template = PollTapeTemplate.get_template()

  # get district
  district = find_value_in_split_result(split_result, "district:")
  template["district"] = district

  # get precinct
  precinct = find_value_in_split_result(split_result, "precinct:")
  template["precinct"] = precinct

  # get date
  date = find_value_in_split_result(split_result, "date:")
  template["date"] = date

  # get time
  time = find_value_in_split_result(split_result, "time:")
  template["time"] = time

  # get ballots cast
  ballots = find_value_in_split_result(split_result, "ballots cast")
  template["ballots_cast"] = ballots

  # get number of votes for each candidate
  for race in template["races"]:
    for candidate in race["candidates"]:
      votes = find_value_in_split_result(split_result, candidate["name"])
      candidate["votes"] = votes

  return template

def find_value_in_split_result(split_result, search_val):
  search_val = search_val.lower()
  val = [i.lower() for i in split_result if i.lower().startswith(search_val)]
  if not val:
    return None
  print(val[0])
  val = val[0].replace(search_val, "")
  val = val.strip()
  return val


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
    try:
      ptparser = PollTapeParser(args.image)
      ptparser.process()
      ocr_result = ptparser.parse()
      final_result = complete_template(ocr_result)
    except ValueError as e:
      return {'error': str(e)}, 409
    return {"output": final_result}

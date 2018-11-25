import pytesseract
from PIL import Image
from io import BytesIO

# Takes in a werkzeug.FileStorage object, converts to an image
# and parses the image into json data
class PollTapeParser:
  def __init__(self, fileobj):
    print(Image.open(BytesIO(fileobj.read())))
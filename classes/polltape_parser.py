import pytesseract
from cv2 import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
import imutils
from skimage.filters import threshold_local

# Takes in a werkzeug.FileStorage object, converts to an image
# and parses the image into json data
class PollTapeParser:
  # Converts werkzeug FileStorage to a PIL Image
  def __init__(self, fileobj):
    # Image as CV2 Array
    buff = fileobj.read()
    nparr = np.fromstring(buff, np.uint8)
    self.cvimg = cv2.imdecode(nparr, 1)


  def showarr(self, arr):
    Image.fromarray(arr).show()

  # returns the detected contour of the poll-tape (4x2)
  def get_paper_contour(self, orig):
    # resize the image for faster computation.
    image = orig.copy()
    ratio = image.shape[0] / 300.0
    image = imutils.resize(image, height = 300)

    # Process the image to find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(gray, 30, 200)

    # Get the ballotContour from the edges -- the largest connected rectangle.
    _, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)[:5]
    ballotContour = None
    for c in contours:
      # approximate the contour
      perimeter = cv2.arcLength(c, True)
      approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    
      # if our approximated contour has four points, then
      # we can assume that we have found our screen
      if len(approx) == 4:
        ballotContour = approx
        break

    if ballotContour is None:
      raise ValueError('image could determine ballot border. make sure the ballot is on a solid dark background, fully in the image.')

    # Draw the contour
    # cv2.drawContours(image, [ballotContour], -1, (0, 255, 0), 1)
    # self.showarr(image)

    # Reshape, scale, and return
    ballotContour = ballotContour.reshape(4,2) * ratio
    return ballotContour

  # Orders a (4x2) matrix s.t:
  # m[0] = top-left point
  # m[1] = top-right point
  # m[2] = bottom-right point
  # m[3] = bottom-left point
  # src = https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
  def order_points(self, contour):
    rect = np.zeros((4,2), dtype='float32')

    # fill top-left and bottom right points
    s = contour.sum(axis=1)
    rect[0] = contour[np.argmin(s)]
    rect[2] = contour[np.argmax(s)]

    # fill the top-right and bottom-left points
    diff = np.diff(contour, axis=1)
    rect[1] = contour[np.argmin(diff)]
    rect[3] = contour[np.argmax(diff)]

    return rect

  # Transforms the original image to a "birds-eye-view" of the poll tape, 
  # using the contour.
  def four_point_transform(self, orig, contour):
    rect = self.order_points(contour)
    print(rect)
    tr, tl, br, bl = rect

    # create the new image width -- the max length of the top or bottom of the contour
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # create the new image height -- the max of the left/right of the contour
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype = "float32")
  
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
    return warped

  # De-skews an image
  # src: https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
  def descew(self):
    contour = self.get_paper_contour(self.cvimg)
    warped = self.four_point_transform(self.cvimg, contour)
    # self.showarr(warped)
    return warped

  # Performs several preprocessing techniques on the tape to increase tesseract accuracy
  def preprocess(self, tape):
    # grayscale
    gray = cv2.cvtColor(tape, cv2.COLOR_BGR2GRAY)
    # skimage threshold (text is a bit light)
    # T = threshold_local(gray, 11, offset = 10)
    # gray = (gray > T).astype("uint8") * 255
    # gray = cv2.medianBlur(gray, 11)
    self.showarr(gray)

    res = cv2.threshold(gray, 80, 255, cv2.THRESH_TOZERO)[1]
    # remove salt and pepper
    res = cv2.medianBlur(gray, 3)
    # self.showarr(res)
    # self.showarr(median)

    return res
    # return gray

  # Does pre-processing on the image to make it easier for pytesseract to read
  def process(self):
    # descew and crop the image so it is only the poll-tape
    tape = self.descew()

    # apply preprocessing to the tape
    processed = self.preprocess(tape)

    # set the PIL Image
    self.image = Image.fromarray(processed)
    
  # Uses pytesseract to convert the image to a string
  def parse(self):
      tess = pytesseract.image_to_string(self.image, lang='eng')
      print(tess)
      return tess

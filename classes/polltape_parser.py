import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
import imutils

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

  # De-skews an image
  # src: https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
  def descew(self):
    image = self.cvimg
    ratio = image.shape[0] / 300.0
    orig = image.copy()
    image = imutils.resize(image, height = 300)
    
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    self.showarr(gray)
    edges = cv2.Canny(gray, 30, 200)
    # self.showarr(edges)

    # Get countours from edges
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

    cv2.drawContours(image, [ballotContour], -1, (0, 255, 0), 3)
    self.showarr(image)

    # create a new mask
    print(image.shape)
    mask = np.zeros((edges.shape[0], edges.shape[1], 3), np.uint8)
    print(mask.shape)
    cv2.drawContours(mask, [ballotContour], -1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    # self.showarr(mask)
    # resize mask to original image size
    mask = imutils.resize(mask, height=orig.shape[0])
    # self.showarr(mask)

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=10)
    mask = cv2.erode(mask, None, iterations=10)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)

    # blend the mask and original image
    mask = mask.astype('float32')/255.0
    img = self.cvimg.astype('float32')/255.0
    masked = (mask * img) + ((1-mask) * (1.0, 1.0, 1.0))
    masked = (masked*255).astype('uint8')
    self.showarr(masked)

    # ROTATION
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # self.showarr(thresh)

    # Calculate bounding-rect and angle of the text
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Correct angle
    angle = -(90 + angle) if angle < -45 else -angle
    print('angle: {}'.format(angle))

    # rotate the image to deskew it
    (h, w) = masked.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(masked, M, (w, h),
      flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

    self.showarr(rotated)

    # crop image to the masked portion
    points = np.column_stack(np.where(gray < 255))
    minx = int(min([p[0] for p in points])//1)
    maxx = int(max([p[0] for p in points])//1)
    miny = int(min([p[1] for p in points])//1)
    maxy = int(max([p[1] for p in points])//1)
    print(minx, maxx, miny, maxy)
    cropped = rotated[minx:maxx, miny:maxy]
    self.showarr(cropped)

    # Apply threshold to cropped image
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    self.showarr(thresh)

    # resize
    self.image = Image.fromarray(thresh)

  # Does post-processing on the image to make it easier for pytesseract to read
  def process(self):
    # De-scew the image
    self.descew()
    
  # Uses pytesseract to convert the image to a string
  def parse(self):
    return pytesseract.image_to_string(self.image)
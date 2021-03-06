# flask imports
from flask import Flask
import flask_restful
from flask_cors import CORS

# api endpoint imports
from endpoints import Hello
from endpoints import OCR
from endpoints import Verified
from endpoints import BulletinBoard
from endpoints import Template
from endpoints import Merger
from endpoints import BBJSON

# Initialize Flask and Flask_Restful apps
app = Flask(__name__)
app.url_map.strict_slashes = False
api = flask_restful.Api(app) 

# Alllow cross origin requests
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Flask app settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max file upload

# Register Flask Restful API endpoints
api.add_resource(Hello, '/api/hello')
api.add_resource(OCR, '/api/ocr')
api.add_resource(Verified, '/api/ocr/verified')
api.add_resource(BulletinBoard, '/api/bulletin')
api.add_resource(Template, '/api/template/<district>')
api.add_resource(Merger, '/api/template/merged')
api.add_resource(BBJSON, '/api/samples/bbjson')

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python3 app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port='8080', debug=True)

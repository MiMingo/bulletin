# flask imports
from flask import Flask
import flask_restful

# api endpoint imports
from endpoints import Hello

# Initialize Flask and Flask_Restful apps
app = Flask(__name__)
app.url_map.strict_slashes = False
api = flask_restful.Api(app)

# Register Flask Restful API endpoints
api.add_resource(Hello, '/api/hello')

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python3 app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='localhost', port='8080', debug=True)
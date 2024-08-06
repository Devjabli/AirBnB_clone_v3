#!/usr/bin/python3
"""
Main application module
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

# Initialize Flask app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

# Enable CORS for specific resources
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_storage(exception):
    """ Close storage connection on teardown """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Return a custom 404 error response """
    return make_response(jsonify({"error": "Not found"}), 404)

# Configure Swagger documentation
app.config['SWAGGER'] = {
    'title': 'AirBnB Clone - RESTful API',
    'description': 'API documentation for the HBNB RESTful API project. All documentation is provided below.',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)

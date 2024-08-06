#!/usr/bin/python3
"""
Module for status and statistics endpoints
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON response with the status of the service
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Retrieves and returns the count of each object type
    """
    counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(counts)

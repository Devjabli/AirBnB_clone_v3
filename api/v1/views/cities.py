#!/usr/bin/python3
"""
Module for handling City-related API endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get.yml', methods=['GET'])
def get_cities(state_id):
    """ Retrieve all cities for a given state ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_id.yml', methods=['GET'])
def get_city(city_id):
    """ Retrieve a specific city by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete.yml', methods=['DELETE'])
def delete_city(city_id):
    """ Delete a specific city by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/post.yml', methods=['POST'])
def create_city(state_id):
    """ Create a new city within a specified state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    data = request.get_json()
    city = City(**data)
    city.state_id = state.id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put.yml', methods=['PUT'])
def update_city(city_id):
    """ Update an existing city by ID """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    storage.save()
    return jsonify(city.to_dict())

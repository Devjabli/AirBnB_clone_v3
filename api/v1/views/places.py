#!/usr/bin/python3
"""
Module for handling Place-related API endpoints
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flasgger.utils import swag_from

@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_places_by_city(city_id):
    """ Retrieve all places associated with a given city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get_id.yml', methods=['GET'])
def get_place(place_id):
    """ Retrieve a specific place by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def delete_place(place_id):
    """ Delete a place by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})

@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_place(city_id):
    """ Create a new place within a given city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def update_place(place_id):
    """ Update an existing place by ID """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    
    storage.save()
    return jsonify(place.to_dict())

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places():
    """ Search for places based on provided criteria """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = set()

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city:
                        places.update(city.places)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    if amenities:
        all_places = list(places)
        places = [place for place in all_places
                  if all(amenity in place.amenities for amenity in amenities)]

    result = [place.to_dict() for place in places]
    for place in result:
        place.pop('amenities', None)
    
    return jsonify(result)

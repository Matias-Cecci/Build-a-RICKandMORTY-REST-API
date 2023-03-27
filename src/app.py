"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Episode, Location
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# ACA EMPEZAMOS LOS ENDPOINTS

# --------------------------USERS--------------------------

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_serialized = [x.serialize() for x in users]
    return jsonify({"body" : user_serialized}), 200


@app.route('/user_register', methods=['POST'])
def user_register():
    body_username = request.json.get("username")
    body_first_name= request.json.get("first_name")
    body_last_name = request.json.get("last_name")
    body_email = request.json.get("email")
    body_password = request.json.get("password")
    user_already_exist = User.query.filter_by(email= body_email).first()
    if user_already_exist:
        return jsonify({"response": "Email already used"}), 300
    new_user = User (username=body_username, first_name=body_first_name, last_name=body_last_name ,email=body_email, password=body_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"response": "User registered successfully"}), 200 

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user_query = User.query.get(user_id)
    if not user_query:
        response_body = {
            "msg" : "This user doesn't exist, can't be deleted."
        }
        return jsonify(response_body), 200
    db.session.delete(user_query)
    db.session.commit()
    response_body = {
        "msg" : "User deleted correctly !"
    }
    return jsonify(response_body), 200

#  --------------------------CHARACTERS--------------------------

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    characters_serialized = [x.serialize() for x in characters]
    return jsonify({"body" : characters_serialized}), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character_query = Character.query.get(character_id)
    
    if not character_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    character_serialize = character_query.serialize()
    return jsonify({"Result": character_serialize}), 200

#  -------------------------- EPISODES --------------------------

@app.route('/episodes', methods=['GET'])
def get_all_episodes():
    episodes = Episode.query.all()
    episodes_serialized = [x.serialize() for x in episodes]
    return jsonify({"body" : episodes_serialized}), 200

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode_by_id(episode_id):
    episode_query = Episode.query.get(episode_id)
    
    if not episode_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    episode_serialize = episode_query.serialize()
    return jsonify({"Result": episode_serialize}), 200

#  ------------- LOCATIONS --------------------------

@app.route('/locations', methods=['GET'])
def get_all_locations():
    locations = Location.query.all()
    locations_serialized = [x.serialize() for x in locations]
    return jsonify({"body" : locations_serialized}), 200


@app.route('/locations/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    location_query = Location.query.get(location_id)
    
    if not location_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    location_serialize = location_query.serialize()
    return jsonify({"Result": location_serialize}), 200

#  ------------- FAVORITES --------------------------

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):
    favorites_characters = User.query.filter_by(id=user_id).first().charactersFav
    favorites_locations = User.query.filter_by(id=user_id).first().locationsFav
    favorites_episodes = User.query.filter_by(id=user_id).first().episodesFav
    Characters = [x.serialize() for x in favorites_characters]
    Locations = [x.serialize() for x in favorites_locations]
    Episodes = [x.serialize() for x in favorites_episodes]

    return jsonify({
        "charactersFav": Characters,
        "locationsFav": Locations,
        "episodesFav": Episodes
    }), 200    


@app.route('/user/<int:user_id>/favorites/character', methods=['GET'])
def get_character_user_favorites(user_id):
    favorites_characters = User.query.filter_by(id=user_id).first().charactersFav
    Characters = [x.serialize() for x in favorites_characters]

    return jsonify({
        "charactersFav": Characters,
    }), 200 


@app.route('/user/<int:user_id>/favorites/location', methods=['GET'])
def get_location_user_favorites(user_id):
    favorites_locations = User.query.filter_by(id=user_id).first().locationsFav
    Locations = [x.serialize() for x in favorites_locations]

    return jsonify({
        "locationsFav": Locations,
    }), 200 


@app.route('/user/<int:user_id>/favorites/episode', methods=['GET'])
def get_episode_user_favorites(user_id):
    favorites_episodes = User.query.filter_by(id=user_id).first().episodesFav
    Episodes = [x.serialize() for x in favorites_episodes]

    return jsonify({
        "episodesFav": Episodes
    }), 200 

# ADD FAVORITE CHARACTER
@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_character_favorite(user_id, character_id):
    
    user = User.query.get(user_id)
    body_character_id = request.json.get("character_id")
    character = Character.query.get(body_character_id)

    user.charactersFav.append(character)

    db.session.commit()

    return jsonify({"response": "Character added to favorites"}), 200

# ADD FAVORITE LOCATION
@app.route('/user/<int:user_id>/favorites/locations/<int:location_id>', methods=['POST'])
def add_location_favorite(user_id, location_id):
    
    user = User.query.get(user_id)
    body_location_id = request.json.get("location_id")
    location = Location.query.get(body_location_id)

    user.locationsFav.append(location)

    db.session.commit()

    return jsonify({"response": "Location added to favorites"}), 200

# ADD FAVORITE EPISODE
@app.route('/user/<int:user_id>/favorites/episodes/<int:episode_id>', methods=['POST'])
def add_episode_favorite(user_id, episode_id):
    
    user = User.query.get(user_id)
    body_episode_id = request.json.get("episode_id")
    episode = Episode.query.get(body_episode_id)

    user.episodesFav.append(episode)

    db.session.commit()

    return jsonify({"response": "Episode added to favorites"}), 200

# DELETE FAVORITE CHARACTER
@app.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def remove_character_favorite(user_id, character_id):
    
    user = User.query.get(user_id)
    body_character_id = Character.query.get(character_id)

    user.charactersFav.remove(body_character_id)

    db.session.commit()

    return jsonify({"response": "Character removed from favorites"}), 200

# DELETE LOCATION CHARACTER
@app.route('/user/<int:user_id>/favorites/locations/<int:location_id>', methods=['DELETE'])
def remove_location_favorite(user_id, location_id):
    
    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    user.locationsFav.remove(location)

    db.session.commit()

    return jsonify({"response": "Location removed from favorites"}), 200


@app.route('/user/<int:user_id>/favorites/episodes/<int:episode_id>', methods=['POST'])
def remove_episode_favorite(user_id, episode_id):
    
    user = User.query.get(user_id)
    episode = Episode.query.get(episode_id)

    user.episodesFav.remove(episode)

    db.session.commit()

    return jsonify({"response": "Episode added to favorites"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

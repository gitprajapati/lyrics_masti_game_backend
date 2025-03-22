from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from flask_restful import Api
from config import DevelopmentConfig
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,get_jwt, JWTManager
from models import User, db, Song
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import genai
import json


load_dotenv()
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)



# -----------------------------------API----------------------------------
api = Api(app)
api.init_app(app)
app.app_context().push()

db.init_app(app)
# ------------------------------Login manager-------------------------

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# ------------------------------JWT-------------------------


jwt = JWTManager(app)



# -----------------------------App Initialisation-------------------------------------

@app.before_request
def create_tables():
    with app.app_context():
        if not path.exists('lyricsmasti.sqlite3'):
            db.create_all()
            
        if not User.query.filter_by(email='admin@test.com').first():
            admin = User(email='admin@test.com', password=generate_password_hash('admin'), role="admin")
            db.session.add(admin)
            db.session.commit()
        if len(Song.query.all()) == 0:
            song_one = Song(title='Shape of You', artist='Ed Sheeran')
            song_two = Song(title='Blinding Lights', artist='The Weeknd')
            song_three = Song(title='Someone Like You', artist='Adele')
            song_four = Song(title='Believer', artist='Imagine Dragons')
            song_five = Song(title='Perfect', artist='Ed Sheeran')
            song_six = Song(title='See You Again', artist='Wiz Khalifa ft. Charlie Puth')
            song_seven = Song(title='Levitating', artist='Dua Lipa ft. DaBaby')
            song_eight = Song(title='Memories', artist='Maroon 5')
            song_nine = Song(title='Senorita', artist='Shawn Mendes & Camila Cabello')
            song_ten = Song(title='Photograph', artist='Ed Sheeran')
            song_eleven = Song(title='Bad Guy', artist='Billie Eilish')
            song_twelve = Song(title='Counting Stars', artist='OneRepublic')
            song_thirteen = Song(title='Despacito', artist='Luis Fonsi ft. Daddy Yankee')
            song_fourteen = Song(title='Stay', artist='The Kid LAROI & Justin Bieber')
            song_fifteen = Song(title='Rolling in the Deep', artist='Adele')
            song_sixteen = Song(title='Cheap Thrills', artist='Sia')
            song_seventeen = Song(title='Dance Monkey', artist='Tones and I')
            song_eighteen = Song(title='Closer', artist='The Chainsmokers ft. Halsey')
            song_nineteen = Song(title='Starboy', artist='The Weeknd ft. Daft Punk')
            song_twenty = Song(title='Love Yourself', artist='Justin Bieber')
            db.session.add(song_one)
            db.session.add(song_two)
            db.session.add(song_three)
            db.session.add(song_four)
            db.session.add(song_five)
            db.session.add(song_six)
            db.session.add(song_seven)
            db.session.add(song_eight)
            db.session.add(song_nine)
            db.session.add(song_ten)
            db.session.add(song_eleven)
            db.session.add(song_twelve)
            db.session.add(song_thirteen)
            db.session.add(song_fourteen)
            db.session.add(song_fifteen)
            db.session.add(song_sixteen)
            db.session.add(song_seventeen)
            db.session.add(song_eighteen)
            db.session.add(song_nineteen)
            db.session.add(song_twenty)
            db.session.commit()




# Direct Register API
@app.route("/direct-register", methods=["POST"])
def direct_register():
    name = "Anonymous"
    role = "temporary"
    new_user = User(role = role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Direct User registered successfully","user": {"role": new_user.role}}), 201


# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401
    user.login_timestamp = datetime.now()
    access_token = create_access_token(identity={"id": user.id})
    return jsonify({"token": access_token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}})



# Logout API
@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    identity = get_jwt_identity()  
    user_id = identity.get("id")  
    if not user_id:
        return jsonify({"error": "Invalid token"}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.logout_timestamp = datetime.now()
    db.session.commit()

    return jsonify(msg="JWT token revoked"), 200



# Create a new song (Admin only)
@app.route("/songs", methods=["POST"])
@jwt_required()
def add_song():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON or missing request body"}), 400
    title = data.get("title", "").strip()
    artist = data.get("artist", "").strip()

    if not isinstance(title, str) or not title:
        return jsonify({"error": "Title must be a non-empty string"}), 400
    if not isinstance(artist, str) or not artist:
        return jsonify({"error": "Artist must be a non-empty string"}), 400

    new_song = Song(title=title, artist=artist)
    db.session.add(new_song)
    db.session.commit()

    return jsonify({
        "message": "Song added successfully",
        "song": {"id": new_song.id, "title": new_song.title, "artist": new_song.artist},
    }), 201

# Get all songs
@app.route("/songs", methods=["GET"])
def get_songs():
    songs = Song.query.all()
    songs_list = [{"id": song.id, "title": song.title, "artist": song.artist} for song in songs]
    return jsonify(songs_list), 200

# Update a song (Admin only)
@app.route("/songs/<int:song_id>", methods=["PUT"])
@jwt_required()
def update_song(song_id):
    data = request.get_json()
    song = Song.query.get(song_id)

    if not song:
        return jsonify({"error": "Song not found"}), 404

    song.title = data.get("title", song.title)
    song.artist = data.get("artist", song.artist)
    db.session.commit()

    return jsonify({"message": "Song updated successfully", "song": {"id": song.id, "title": song.title, "artist": song.artist}}), 200

# Delete a song (Admin only)
@app.route("/songs/<int:song_id>", methods=["DELETE"])
@jwt_required()
def delete_song(song_id):
    song = Song.query.get(song_id)

    if not song:
        return jsonify({"error": "Song not found"}), 404

    db.session.delete(song)
    db.session.commit()

    return jsonify({"message": "Song deleted successfully"}), 200



# Generate Lyrics using Gemini
@app.route("/generate-lyrics", methods=["GET"])
def generate_lyrics():
    song = Song.query.order_by(db.func.random()).first()
    if not song:
        return jsonify({"error": "No songs available in the database."}), 404

    model = genai.GenerativeModel('gemini-2.0-flash', generation_config={"response_mime_type": "application/json"})
    prompt =f"""Retrieve and analyze the lyrics for song with title name '{song.title}' by artist name {song.artist}.
    Just Provide first four lines of songs lyrics.
    Exclude title and artist names from the response.
    Use this JSON schema:
    - {{lyrics_snippet}}: Just Provide first four lines of songs lyrics.""",
    response = model.generate_content(prompt)
    response_data = json.loads(response.text)
    lyrics_snippet = response_data.get('lyrics_snippet', '')

    return jsonify({
        "title": song.title,
        "artist": song.artist,
        "generated_lyrics": lyrics_snippet
    })


if __name__ == "__main__":
    print("Flask app is starting...")
    app.run(debug=True) 
import os
from flask import Blueprint, request
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from core.facerecognition import process_photo
from app.models import Photo, db


api_bp= Blueprint("api", __name__)
api = Api(api_bp)

# Datos para albums, usuarios y fotos
users={}
albums={}
photos={}

# Argumentos del parser
parser=reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of the resource")
parser.add_argument("email", type=str, help="Email of the user")
parser.add_argument("age", type=int, help="Age of the user")
parser.add_argument("title", type=str, help="Title of the album")
parser.add_argument("filename", type=str, help="Filename of the photo")
parser.add_argument("album_id", type=int, help="ID of the album")

class UserList(Resource):
    @jwt_required()
    def get(self):
        return {
            user_id: {"name":user["name"]} for user_id, user in users.items()
        }

class User(Resource):
    @jwt_required()
    def get(self, user_id):
        return users[user_id]
    
    @jwt_required()
    def put(self, user_id):
        args=parser.parse_args()
        user={
            "name": args["name"],
            "email": args["email"],
            "age": args["age"]
        }
        users[user_id]=user
        return user, 200
    
    @jwt_required()
    def delete(self, user_id):
        del users[user_id]
        return "", 204

class AlbumList(Resource):
    @jwt_required()
    def get(self):
        return albums
    
    @jwt_required()
    def post(self):
        args=parser.parse_args()
        album_id=int(max(albums.keys() or [0]))+1
        albums[album_id]={
            "title": args["title"]
        }
        return albums[album_id], 201

class Album(Resource):
    @jwt_required()
    def get(self, album_id):
        return albums[album_id]

    @jwt_required()
    def put(self, album_id):
        args=parser.parse_args()
        album={
            "title": args["title"]
        }
        albums[album_id]=album
        return album, 200

    @jwt_required()
    def delete(self, album_id):
        del albums[album_id]
        return "", 204

class PhotoList(Resource):
    @jwt_required()
    def get(self):
        return photos
    
    @jwt_required()
    def post(self):
        args=parser.parse_args()
        photo_id=int(max(photos.keys() or [0])) + 1
        file=request.files["file"]
        filename=secure_filename(file.filename)
        filepath=os.path.join("uploads", filename)
        file.save(filepath)

        photo= Photo(
            id=photo_id,
            filename=filename,
            original_filename=filename,
            path=filepath,
            user_id=args["user_id"],
            album_id=args["album_id"]
        )
        db.session.add(photo)
        db.session.commit()

        # Procesar la foto para detectar rostros
        process_photo(photo)

        photos[photo_id]={
            "filename": args["filename"],
            "album_id": args["album_id"]
        }
        return photos[photo_id], 201

class Photo(Resource):
    @jwt_required()
    def get(self, photo_id):
        return photos[photo_id]
    
    @jwt_required()
    def put(self, photo_id):
        args=parser.parse_args()
        photo={
            "filename": args["filename"],
            "album_id": args["album_id"]
        }
        photos[photo_id]=photo
        return photo, 200
    
    @jwt_required()
    def delete(self, photo_id):
        del photos[photo_id]
        return "", 204

# Rutas de la API
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(AlbumList, '/albums')
api.add_resource(Album, '/albums/<int:album_id>')
api.add_resource(PhotoList, '/photos')
api.add_resource(Photo, '/photos/<int:photo_id>')
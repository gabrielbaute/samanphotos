import face_recognition
from app.models import Photo, FaceEncoding, db

def process_photo(photo):
    """Procesa una foto para detectar y almacenar codificaciones faciales"""
    image=face_recognition.load_image_file(photo.path)
    face_location=face_recognition.face_locations(image)
    face_encodings=face_recognition.face_encodings(image, face_location)

    for enconding in face_encodings:
        face_encoding=FaceEncoding(
            enconding=enconding,
            photo_id=photo.id
        )
        db.session.add(face_encoding)
    db.session.commit()
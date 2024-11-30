import face_recognition
from app.models import Photo, FaceEncoding, db

def process_photo(photo):
    """Procesa una foto para detectar y almacenar codificaciones faciales"""
    image = face_recognition.load_image_file(photo.path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # Obtener todas las codificaciones faciales existentes
    try:
        existing_encodings = FaceEncoding.query.all()
        existing_encodings_list = [face.encoding for face in existing_encodings]
    except Exception as e:
        existing_encodings_list = []

    for encoding, location in zip(face_encodings, face_locations):
        # Comparar con las codificaciones existentes si las hay
        if existing_encodings_list:
            matches = face_recognition.compare_faces(existing_encodings_list, encoding)
        else:
            matches = []

        if True not in matches:
            # Si no hay coincidencias, guardar la nueva codificación y las coordenadas
            top, right, bottom, left = location
            face_encoding = FaceEncoding(
                encoding=encoding,
                photo_id=photo.id,
                top=top,
                right=right,
                bottom=bottom,
                left=left
            )
            db.session.add(face_encoding)
    db.session.commit()

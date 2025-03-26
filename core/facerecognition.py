import face_recognition
import numpy as np
from database.models import Photo, FaceEncoding
from app.extensions import db

def detect_faces(photo):
    """Detecta rostros en una foto y devuelve las codificaciones y ubicaciones"""
    image=face_recognition.load_image_file(photo.path)
    face_locations=face_recognition.face_locations(image)
    face_encodings=face_recognition.face_encodings(image, face_locations)
    return face_encodings, face_locations

def process_encodings(photo, face_encodings, face_locations):
    """Verifica las coincidencias y guarda las nuevas codificaciones faciales"""
    try:
        existing_encodings=FaceEncoding.query.all()
        existing_encodings_list=[np.array(face.encoding) for face in existing_encodings]
    except Exception as e:
        existing_encodings_list=[]

    for encoding, location in zip(face_encodings, face_locations):
        if existing_encodings_list:
            matches=face_recognition.compare_faces(existing_encodings_list, encoding)
        else:
            matches=[]

        if True not in matches:
            top, right, bottom, left = location
            face_encoding=FaceEncoding(
                encoding=encoding.tolist(),
                photo_id=photo.id,
                top=top,
                right=right,
                bottom=bottom,
                left=left
            )
            db.session.add(face_encoding)
    db.session.commit()

def process_photo(photo):
    """Procesa una foto completa"""
    face_encodings, face_locations=detect_faces(photo)
    if not face_encodings:
        return # Si no se detectan codificaciones, no continuar
    process_encodings(photo, face_encodings, face_locations)

def comparefaces(target_encoding, tolerance=0.9):
    """Compara una codificación facial objetivo con todas las codificaciones faciales en la base de datos"""
    all_faces = FaceEncoding.query.all()
    print(f"Comparando con {len(all_faces)} codificaciones faciales en la base de datos.")
    matches = []
    for face in all_faces:
        face_encoding_array = np.array(face.encoding)
        print(f"Codificación objetivo: {target_encoding}")
        print(f"Codificación del rostro {face.id}: {face_encoding_array}")
        is_match = face_recognition.compare_faces([target_encoding], face_encoding_array, tolerance=tolerance)
        print(f"Comparando con rostro {face.id}: {'Match' if True in is_match else 'No Match'}")
        if True in is_match:
            matches.append(face)
    return matches
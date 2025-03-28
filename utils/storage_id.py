import uuid

def generate_storage_user_id():
    """user_id para generar ruta de almacenamiento"""
    
    storage_user_id = (uuid.uuid4().hex)
    return storage_user_id
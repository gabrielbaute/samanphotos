import os
import uuid
from flask import current_app

def create_user_storage(storage_user_id):
    storage_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"user_{uuid.uuid4().hex}_{storage_user_id}")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    return storage_path

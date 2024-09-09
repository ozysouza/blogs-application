from flask import request, jsonify, Blueprint, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from src.website.auth import logger

upload = Blueprint('upload', __name__)


@upload.route('/upload-image', methods=['GET', 'POST'])
@login_required
def upload_image():
    if 'upload' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['upload']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Ensure the upload folder exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        user_name = f'{current_user.first_name}-{current_user.last_name}'
        user_folder = os.path.join(upload_folder, user_name)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            logger.info(f'Folder created: {user_folder}')

        file_path = os.path.join(user_folder, filename)
        try:
            file.save(file_path)
            file_url = url_for('static',
                               filename=f'uploads/users/{current_user.first_name}-{current_user.last_name}/{filename}',
                               _external=True)
            logger.info(f'Image added into: {file_url}')

            return jsonify({"url": file_url})
        except Exception as err:
            logger.error(f"Error: {err}")
            return jsonify({"error": str(err)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

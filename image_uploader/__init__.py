from flask import Flask, jsonify
from flask_restful import Api
from image_uploader.upload import UploadImage
from image_uploader.exceptions import BaseExceptions

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG'])


api = Api(app)
api.add_resource(UploadImage, '/upload', '/images/<filename>')


@app.errorhandler(BaseExceptions)
def handle_exception(error):
    data = {
        "code": error.code,
        "reason": error.message,
        "extra_info": error.extra
    }
    response = jsonify(data)
    response.status_code = error.status_code
    return response

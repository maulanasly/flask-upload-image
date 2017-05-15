import os
from flask import send_from_directory, current_app
from flask_restful import Resource, reqparse
from werkzeug import secure_filename, datastructures
from image_uploader.exceptions import InvalidFileType


upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=datastructures.FileStorage, location='files')


class UploadImage(Resource):

    # For a given file, return whether it's an allowed type or not
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        # Check if the file is one of the allowed types/extensions
        if file and self.allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            return {'filename': filename}, 200
        else:
            raise InvalidFileType

    def get(self, filename):
        root_dir = os.path.dirname(os.getcwd())
        return send_from_directory(os.path.join(root_dir, 'flask-upload-image/uploads'), filename)
        # return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, mimetype='image/png')

import sys

from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)
api = Api(app)
root_path = os.path.join(sys.path[0],"uploads")
# Serve Swagger JSON file from the 'static' directory
@app.route('/static/swagger.json')
def send_swagger_json():
    return send_from_directory('static', 'swagger.json')

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Set of allowed file extensions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadERPExcel(Resource):
    def post(self):
        """
        Uploads an ERP Excel file.
        ---
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: file
            type: file
            required: true
            description: The Excel file to be uploaded.
        responses:
          200:
            description: File uploaded successfully.
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
          400:
            description: Bad Request - Invalid file type.
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
        """
        try:
            uploaded_file = request.files['file']

            if uploaded_file and allowed_file(uploaded_file.filename):
                file_path = os.path.join(f'{root_path}', uploaded_file.filename)
                uploaded_file.save(file_path)
                return jsonify({"success": True, "message": "File uploaded successfully"})
            else:
                return jsonify({"success": False, "message": "Invalid file. Please upload an Excel file (xlsx or xls)."}), 400

        except Exception as e:
            return jsonify({"success": False, "message": str(e)})

api.add_resource(UploadERPExcel, '/upload_erp_excel')

# Use the correct URL for Swagger JSON in the Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'  # This should match the route where you serve the Swagger JSON
API_NAME = "upload excel file"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': API_NAME
    }
)

app.register_blueprint(swaggerui_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

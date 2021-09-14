import cloudinary
import cloudinary.uploader
from flask import request, jsonify
from flask_cors import CORS, cross_origin



#cloudinary
CORS(app)

def upload_file(app):
  app.logger.info('in upload route')
  cloudinary.config( 
    cloud_name = "dtdhdix1f", 
    api_key = "546218847156792", 
    api_secret = "ects6SDSdPX94um0t3sIpp-uJgk" 
    )
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['projectImage']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(
          file_to_upload,
          folder = "feedback-app/", 

          )
      app.logger.info(upload_result)
      uploade_img_url = upload_result["secure_url"]
    return upload_result["secure_url"]
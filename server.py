import cv2 as cv
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from api.CatRecognition import CheckImage, AddNewClass


app = Flask(__name__, 
	static_url_path='',
	static_folder='website')

CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


def get_api_error_response(message, code):
    return jsonify({'message': message}), code


def readb64(encoded_data):
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/cat_recognition_api/v1/actions/get_response', methods=['POST'])
def get_model_response():
	params = request.get_json()
	try:
		image = readb64(params.get('image'))
		return jsonify({'response': CheckImage(image)})
	except KeyError as e:
		return get_api_error_response('Malformed request, no "%s" param was found' % str(e), 400)
	except ValueError as e:
		return get_api_error_response('Malformed request: %s' % str(e), 400)


@app.route('/cat_recognition_api/v1/actions/add_new_profile', methods=['POST'])
def get_model_response():
	params = request.get_json()
	try:
		image = readb64(params.get('image'))
		return jsonify({'response': AddNewClass([image])})
	except KeyError as e:
		return get_api_error_response('Malformed request, no "%s" param was found' % str(e), 400)
	except ValueError as e:
		return get_api_error_response('Malformed request: %s' % str(e), 400)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

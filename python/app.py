from flask import Flask, render_template, request, jsonify, url_for, make_response, json
from flask_uploads import UploadSet, configure_uploads, IMAGES
from Tkinter import *
from PIL import Image, ExifTags
import pytesseract
import urllib
import requests
import json
from flask_cors import CORS, cross_origin
import os
#import filetype
import time
import fileinput
from werkzeug import secure_filename
import string
import re
import sys
import operator
import io
import os
import darknet
#from Tkinter import * 

#PEOPLE_FOLDER = os.path.join('static', 'people_photo')

application = Flask(__name__,static_url_path='/static')
CORS(application, support_credentials=True)

photos = UploadSet('photos', IMAGES)
application.config['UPLOADED_PHOTOS_DEST'] = './static'

@application.route('/index', methods=['GET', 'POST'])
def show_index():
    full_filename = os.path.join(application.config['UPLOADED_PHOTOS_DEST'], 'image.jpg')
    return render_template("index.html", user_image = full_filename)

@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        fullpath = file.filename    
        file.save(secure_filename(fullpath))
        image=Image.open(fullpath)
        image.save(fullpath)
        result = darknet.detect_image(fullpath)
        link = "./image.jpg" 
        test = json.dumps({"result": result, "resultimage":link},sort_keys = True, indent = 4, separators = (',', ': '))


        full_filename = os.path.join(application.config['UPLOADED_PHOTOS_DEST'], 'image.jpg')
        return render_template("index.html",user_image = full_filename, test = test)
        
     
@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')



@application.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('landing.html')



if __name__ == '__main__':

    application.run(debug=True, port=80, host="0.0.0.0")


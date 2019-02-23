from flask import Flask, render_template, request, jsonify, url_for, make_response, json
from flask_uploads import UploadSet, configure_uploads, IMAGES
from Tkinter import *
from PIL import Image, ExifTags
import pytesseract
import urllib
import requests
import json
from flask_cors import CORS, cross_origin
import os, sys, shutil
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
import random
import detectcv2 as dcv
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
        #image=Image.open(fullpath)
        #image.save(fullpath)
        imageFileName = ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.jpg'
        full_filename = os.path.join(application.config['UPLOADED_PHOTOS_DEST'], imageFileName)
        result = dcv.detect_image(fullpath, imageFileName,full_filename)
        
        #result1 = darknet.detect_image(fullpath, imageFileName)
<<<<<<< HEAD
        test = json.dumps({"result": result},sort_keys = True, indent = 4, separators = (',', ': '))
        
        return render_template("index.html",user_image = imageFileName, test = test)
=======
        #test = json.dumps({"result": result},sort_keys = True, indent = 4, separators = (',', ': '))
        
        return render_template("index.html",user_image = imageFileName)
>>>>>>> ae2165a48199206d3660c20523c0e905ef026e9c
     
@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')



@application.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('landing.html')



if __name__ == '__main__':

    application.run(debug=True, port=80, host="0.0.0.0")


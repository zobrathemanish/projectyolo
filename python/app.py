from flask import Flask, render_template, request, jsonify
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

application = Flask(__name__,static_url_path='/static')
CORS(application, support_credentials=True)

photos = UploadSet('photos', IMAGES)
application.config['UPLOADED_PHOTOS_DEST'] = 'static/img'

@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        fullpath = file.filename    
        file.save(secure_filename(fullpath))
        image=Image.open(fullpath)
        image.save(fullpath)
        result = darknet.detect_image(fullpath)
        image = Image.open('./image.jpg')
        image.show()
        print image
        return jsonify({"result": result})
     
@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')


@application.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('landing.html')



if __name__ == '__main__':

    application.run(debug=True, port=80, host="0.0.0.0")


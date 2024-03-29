from flask import Flask, render_template, request, jsonify, url_for, make_response, json, redirect
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
from flask_mysqldb import MySQL 
import yaml
#from Tkinter import * 

#PEOPLE_FOLDER = os.path.join('static', 'people_photo')

application = Flask(__name__,static_url_path='/static')
CORS(application, support_credentials=True)

photos = UploadSet('photos', IMAGES)
application.config['UPLOADED_PHOTOS_DEST'] = './static'

db = yaml.load(open('db.yaml'))

application.config['MySQL_HOST'] = db['mysql_host']
application.config['MySQL_USER'] = db['mysql_user']
application.config['MySQL_PASSWORD'] = db['mysql_password']
application.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(application)


@application.route('/index', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #fetch form data
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        email = userDetails['email']
        photo = userDetails['photo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,password,email,photo) VALUES(%s, %s, %s, %s)",(name,password,email,photo))
        mysql.connection.commit()
        cur.close()
        return redirect ('/users')
    return render_template('landing2.html')

@application.route('/users')
def users():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        fullpath = file.filename    
        file.save(secure_filename(fullpath))
        image=Image.open(fullpath)
        image.save(fullpath)

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()

        return render_template('users.html', userDetails = userDetails)

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
        test = json.dumps({"result": result},sort_keys = True, indent = 4, separators = (',', ': '))
        
        return render_template("index.html",user_image = imageFileName, test = test)
     
@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')




@application.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('landing.html')



if __name__ == '__main__':

    application.run(debug=True, port=80, host="0.0.0.0")


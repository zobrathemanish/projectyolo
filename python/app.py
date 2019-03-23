from flask import Flask, render_template, request, jsonify, url_for, make_response, json, redirect, flash
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
import matchfiles as match
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
        photo = request.files['photo']
        fullpath = photo.filename
        full_filename = ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.jpg'
        photo.save(secure_filename(full_filename))
        cur = mysql.connection.cursor()
        x = cur.execute("SELECT photo FROM users WHERE name =%s", [name])
        if int(x)>0:
            flash("Username taken")
            print "Username taken"
            return render_template("usernametaken.html")
        else:
            cur.execute("INSERT INTO users(name,password,email,photo) VALUES(%s, %s, %s, %s)",(name,password,email,full_filename))
        mysql.connection.commit()
        cur.close()
        return redirect ('/users')

    return render_template('landing2.html')

@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/loginemail')
def loginemail():
	return render_template('emaillogin.html')

@application.route('/users')
def users():
        return render_template('users.html')

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

@application.route('/upload_FID', methods=['GET', 'POST'])
def upload_FID():
    if request.method == 'POST':
        username = request.form['name']
        file = request.files['photo']
        newimg = file.filename    
        file.save(secure_filename(newimg))
        cur = mysql.connection.cursor()
        cur.execute("SELECT photo FROM users WHERE name =%s", [username])
        userDetails = cur.fetchone()
        try:
        	oldimg = userDetails[0]
        except TypeError:
        	stmt = 'No such username found'
        	return json.dumps(stmt)
        #oldimg = userDetails[0]
        mysql.connection.commit()
        cur.close()
        verified1 = match.verify(newimg, oldimg)
        #verified = "[" + verified1.replace("}", "},", verified1.count("}")-1) + "]"
        json_data = json.loads(verified1)
        result = json.dumps({"result": json_data},sort_keys = True, indent = 4, separators = (',', ': '))
        #resp = json_data.to_dict()
       # print json_data['score']
        percent = json_data['score'] *100
        if percent>90:
             return render_template("index2.html", result = result)
        else:
             return render_template("matchfailed.html")

@application.route('/upload_EID', methods=['GET', 'POST'])
def upload_EID():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT * FROM users WHERE email =%s AND password = %s", [email,password])
      	print value
        if int(value)>0:
        	stmt = "Welcome to the page. Verified Successfully."
        	return json.dumps(stmt)
        else:
        	stmt = "Authentication error"
        	return json.dumps(stmt)
        mysql.connection.commit()
        cur.close()

@application.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')


@application.route('/viewdatabase', methods=['GET', 'POST'])
def test():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()

    return render_template('userdatabaselist.html',userDetails = userDetails)


@application.route('/camdetection', methods=['GET', 'POST'])
def camdetection():
    return render_template('camdetection.html')

if __name__ == '__main__':
    application.secret_key = 'some_secret'

    application.run(debug=True, port=80, host="0.0.0.0")


from flask import Flask, json,redirect,render_template,flash,request, jsonify
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from firebase_admin import db
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user

# import jsonify
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials, storage, db as fire_db


import pyrebase

config = {
  "apiKey": "AIzaSyAf0_8CIFXTktEuKyi2-ew3qb_NdmveQ1U",
  "authDomain": "emergencybooking-31043.firebaseapp.com",
  "databaseURL": "https://emergencybooking-31043-default-rtdb.firebaseio.com",
  "projectId": "emergencybooking-31043",
  "storageBucket": "emergencybooking-31043.appspot.com",
  "messagingSenderId": "861314242227",
  "appId": "1:861314242227:web:138c0463732d118f6b42c6",
  "measurementId": "G-KXVD03V691"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
 # Initialize Firebase with your service account credentials
cred = credentials.Certificate("project/emergencybooking-31043-firebase-adminsdk-l69k0-f7411c864f.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'emergencybooking-31043.appspot.com'
})


#database connection
local_server=True
app=Flask(__name__)
app.secret_key="aneesrehmankhan"






# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databsename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/emergency_bed_booking_system'
dbsql=SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Hospitaluser.query.get(int(user_id))


class Test(dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    name=dbsql.Column(dbsql.String(50))


class User(UserMixin,dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    email=dbsql.Column(dbsql.String(50))
    dob=dbsql.Column(dbsql.String(1000))



class Hospitaluser(UserMixin,dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    hcode=dbsql.Column(dbsql.String(20))
    email=dbsql.Column(dbsql.String(50))
    password=dbsql.Column(dbsql.String(1000))


class Hospitaldata(dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    hcode=dbsql.Column(dbsql.String(20),unique=True)
    hname=dbsql.Column(dbsql.String(100))
    normalbed=dbsql.Column(dbsql.Integer)
    hicubed=dbsql.Column(dbsql.Integer)
    icubed=dbsql.Column(dbsql.Integer)
    vbed=dbsql.Column(dbsql.Integer)

class Trig(dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    hcode=dbsql.Column(dbsql.String(20))
    normalbed=dbsql.Column(dbsql.Integer)
    hicubed=dbsql.Column(dbsql.Integer)
    icubed=dbsql.Column(dbsql.Integer)
    vbed=dbsql.Column(dbsql.Integer)
    querys=dbsql.Column(dbsql.String(50))
    date=dbsql.Column(dbsql.String(50))

class Bookingpatient(dbsql.Model):
    id=dbsql.Column(dbsql.Integer,primary_key=True)
    bedtype=dbsql.Column(dbsql.String(100))
    hcode=dbsql.Column(dbsql.String(20))
    spo2=dbsql.Column(dbsql.Integer)
    pname=dbsql.Column(dbsql.String(100))
    pphone=dbsql.Column(dbsql.String(100))
    paddress=dbsql.Column(dbsql.String(100))
    email=dbsql.Column(dbsql.String(50), unique=True, nullable=False)
    # plink = dbsql.Column(dbsql.String(255))



@app.route("/")
def home():
   
    return render_template("index.html")


import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import spacy
import random
import json

# Load English tokenizer, tagger, parser, NER, and word vectors
# nlp = spacy.load("en_core_web_sm")

# Sample dataset containing disease information
data_file = open('project/dataset.json').read()
dataset = json.loads(data_file)


# # Function to generate response based on user input
# def generate_response(user_input):
#     doc = nlp(user_input)
#     for token in doc:
#         if token.dep_ == "nsubj" and token.head.text == "recommend":
#             disease = token.text
#             for item in dataset:
#                 if item["disease"].lower() == disease.lower():
#                     return f"For {disease}, the recommended bed type is {item['recommended_bedtype']}."
#         elif "bed" in user_input.lower():
#             for item in dataset:
#                 if item["disease"].lower() in user_input.lower():
#                     return f"For {item['disease']}, the recommended bed type is {item['recommended_bedtype']}."
#     for item in dataset:
#         if item["disease"].lower() in user_input.lower():
#             return f"Treatment Options: {item['treatment_options']}\n*Post Admission Care:* {item['post_admission_care']}\n*Suggested bed:* {item['recommended_bedtype']}"
#     return "Sorry, I couldn't understand your query."




# Load dataset containing disease information
with open('project/dataset.json', 'r') as file:
    dataset = json.load(file)


disease = None
@app.route('/start', methods=['POST'])
def start():
    global disease
    option = request.json['input'].lower()
    
    # Check if the specified disease exists in the dataset
    for item in dataset:
        if item["disease"].lower() == option:
            disease = option
            response = "Options:\n"
            response += "1) Treatment Options\n"
            response += "2) Post Admission Care\n"
            response += "3) Recommend Bed Type\n"
            response += "4) Check another\n"
            return jsonify({'response': response})
        elif option == "1":
            for item in dataset:
                if item["disease"].lower() == disease:
                    return jsonify({'response': f"Treatment Options for {disease}: {item['treatment_options']}"})
        elif option == "2":
            for item in dataset:
                if item["disease"].lower() == disease:
                    return jsonify({'response': f"Post Admission Care for {disease}: {item['post_admission_care']}"})
        elif option == "3":
            for item in dataset:
                if item["disease"].lower() == disease:
                    return jsonify({'response': f"For {disease}, the recommended bed type is {item['recommended_bedtype']}."})
    return jsonify({'response': "Assistant: The specified disease is not found in the dataset."})


@app.route("/trigers")
def trigers():
    query=Trig.query.all() 
    return render_template("trigers.html",query=query)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        dob=request.form.get('dob')
        encpassword=generate_password_hash(dob)
        emailUser=User.query.filter_by(email=email).first()
        if emailUser:
            flash("Email id is already taken","warning")
            return render_template("usersignup.html")
        new_user=User(email=email,dob=encpassword)
        dbsql.session.add(new_user)
        dbsql.session.commit()
                
        flash("SignUp Success Please Login","success")
        return render_template("userlogin.html")

    return render_template("usersignup.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        dob=request.form.get('dob')
        emailUser=User.query.filter_by(email=email).first()
        if emailUser and check_password_hash(emailUser.dob,dob):
            login_user(emailUser)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")


    return render_template("userlogin.html")

@app.route('/chat',methods=['POST','GET'])
def chat_ass():
    return render_template("chat_ass.html")

@app.route('/hospitallogin',methods=['POST','GET'])
def hospitallogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=Hospitaluser.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("hospitallogin.html")


    return render_template("hospitallogin.html")

@app.route('/admin',methods=['POST','GET'])
def admin():
 
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if(username=="admin" and password=="admin"):
            session['user']=username
            flash("login success","info")
            return render_template("addHosUser.html")
        else:
            flash("Invalid Credentials","danger")

    return render_template("admin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addHospitalUser',methods=['POST','GET'])
def hospitalUser():
   
    if('user' in session and session['user']=="admin"):
      
        if request.method=="POST":
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            hcode=hcode.upper()      
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email is already taken","warning")
         
            # dbsql.engine.execute(f"INSERT INTO hospitaluser (hcode,email,password) VALUES ('{hcode}','{email}','{encpassword}') ")
            query=Hospitaluser(hcode=hcode,email=email,password=encpassword)
            dbsql.session.add(query)
            dbsql.session.commit()

            # my mail starts from here if you not need to send mail comment the below line
           
            # mail.send_message('COVID CARE CENTER',sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","warning")
            return render_template("addHosUser.html")

    else:
        flash("Login and try Again","warning")
        return render_template("addHosUser.html")
    


# testing wheather dbsql is connected or not  
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'

@app.route("/logoutadmin")
def logoutadmin():
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect('/admin')


def updatess(code):
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()
    return render_template("hospitaldata.html",postsdata=postsdata)

@app.route("/addhospitalinfo",methods=['POST','GET'])
def addhospitalinfo():
    print(current_user)
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    # if not posts:
    #     return redirect('/admin')
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        hduser=Hospitaldata.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        if huser:            
            # dbsql.engine.execute(f"INSERT INTO hospitaldata (hcode,hname,normalbed,hicubed,icubed,vbed) VALUES ('{hcode}','{hname}','{nbed}','{hbed}','{ibed}','{vbed}')")
            query=Hospitaldata(hcode=hcode,hname=hname,normalbed=nbed,hicubed=hbed,icubed=ibed,vbed=vbed)
            dbsql.session.add(query)
            dbsql.session.commit()
            flash("Data Is Added","primary")
            return redirect('/addhospitalinfo')
            

        else:
            flash("Hospital Code not Exist","warning")
            return redirect('/addhospitalinfo')




    return render_template("hospitaldata.html",postsdata=postsdata)


@app.route("/hedit/<string:id>",methods=['POST','GET'])
@login_required
def hedit(id):
    posts=Hospitaldata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        # dbsql.engine.execute(f"UPDATE hospitaldata SET hcode ='{hcode}',hname='{hname}',normalbed='{nbed}',hicubed='{hbed}',icubed='{ibed}',vbed='{vbed}' WHERE hospitaldata.id={id}")
        post=Hospitaldata.query.filter_by(id=id).first()
        post.hcode=hcode
        post.hname=hname
        post.normalbed=nbed
        post.hicubed=hbed
        post.icubed=ibed
        post.vbed=vbed
        dbsql.session.commit()
        flash("Slot Updated","info")
        return redirect("/addhospitalinfo")

    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hdelete(id):
    # dbsql.engine.execute(f"DELETE FROM hospitaldata WHERE hospitaldata.id={id}")
    post=Hospitaldata.query.filter_by(id=id).first()
    dbsql.session.delete(post)
    dbsql.session.commit()
    flash("Date Deleted","danger")
    return redirect("/addhospitalinfo")



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Upload file to Firebase Storage
    storage.child("uploads/" + file.filename).put(file)
      # Get the download URL of the uploaded file
    download_url = storage.child("uploads/" + file.filename).get_url(None)

    # Store the download URL in the session
    session['download_url'] = download_url
    if current_user.is_authenticated:
        email = current_user.email
        booking_patient = Bookingpatient.query.filter_by(email=email).first()
        # if booking_patient:
        #     booking_patient.plink = download_url
        #     dbsql.session.commit()
        #     flash("File uploaded successfully.", "success")
        # else:
        #     flash("Booking patient not found.", "error")
    else:
        flash("User not authenticated.", "error")
    return render_template("base.html")

@app.route("/view_pdf", methods=["GET"])
@login_required
def view_pdf():
    # Retrieve the PDF file name from the session
    download_url = session.get('download_url',None)

    if download_url:
        return render_template("view_pdf.html", download_url=download_url)
    else:
        flash("PDF file not found.", "danger")
        return redirect(url_for("pdetails"))

@app.route("/pdetails", methods=['GET'])
@login_required
def pdetails():
    email = current_user.email
    user = Hospitaluser.query.filter_by(email=email).first()
    if not user:
        flash("User not found.", "error")
        return redirect('/admin')

    code = user.hcode
    booking_patient = Bookingpatient.query.filter_by(hcode=code).first()
    if not booking_patient:
        flash("Booking patient not found.", "error")
        return redirect('/admin')

    # download_url = booking_patient.plink
    return render_template("detials.html", data=booking_patient)




@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbookig():
    query1=Hospitaldata.query.all()
    query=Hospitaldata.query.all()
    if request.method=="POST":
        
        email=request.form.get('email')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospitaldata.query.filter_by(hcode=hcode).first()
        checkpatient=Bookingpatient.query.filter_by(email=email).first()
        
        if checkpatient:
            flash("already email id is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        dbsqlb=Hospitaldata.query.filter_by(hcode=hcode).first()      
        bedtype=bedtype
        if bedtype=="NormalBed":       
            # bb
            seat=dbsqlb.normalbed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.normalbed=seat-1
            dbsql.session.commit()
                
            
        elif bedtype=="HICUBed":      
            # for d in dbsqlb:
            seat=dbsqlb.hicubed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.hicubed=seat-1
            dbsql.session.commit()

        elif bedtype=="ICUBed":     
            # for d in dbsqlb:
            seat=dbsqlb.icubed
            print(seat)
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.icubed=seat-1
            dbsql.session.commit()

        elif bedtype=="VENTILATORBed": 
            # for d in dbsqlb:
            seat=dbsqlb.vbed
            ar=Hospitaldata.query.filter_by(hcode=code).first()
            ar.vbed=seat-1
            dbsql.session.commit()
        else:
            pass

        check=Hospitaldata.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Bookingpatient(bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress,email=email)
                dbsql.session.add(res)
                dbsql.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("upload_file.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("booking.html",query=query,query1=query1)

  



@app.route("/recommend", methods=["GET", "POST"])
def recommend_bed():
    if request.method == "POST":
        disease = request.form["disease"]
        recommendations = recommend_bed_by_disease(disease)

        if recommendations:
            return render_template(
                "index.html", disease=disease, recommendations=", ".join(recommendations)
            )
        else:
            return render_template("index.html", disease=disease, recommendations="Not Found")
    else:
        return render_template("index.html")

    
app.run(debug=True)


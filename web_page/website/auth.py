import array
from flask import Blueprint , render_template , request , redirect , url_for , jsonify
from .models import User , Note
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user
from email.message import EmailMessage
import ssl
import smtplib
import random
import json

from dotenv import load_dotenv
import os

scores = {} ; sum = 0 ; max = -1000 ; code = random.randint(100000 , 999999)


auth = Blueprint('auth' , __name__)



#logout


@auth.route('/logout' )
def logout():
    logout_user()
    return redirect('/')



#sign_up

@auth.route('/sign_up' , methods = ["POST" , "GET"])

def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')


        #email sending

        load_dotenv()

        VIDEO_PATH = r"C:\Users\kzlat\Desktop\Nasa_space_app_challenge\Space-Soup\generated_audios\generated_audio.mp3"


        PASSWORD = os.getenv("EMAIL_PASS")
        print(PASSWORD)

       # emails = User.query.filter_by(email = email).first()

        email_sender = 'kzlatev07@gmail.com'
        email_password = PASSWORD
        email_receiver = ["kzlatev07@gmail.com", "vzlatev7@gmail.com"]

        subject = "Verification code"

        global code

        body = f"""
        to prossed enter this verification code in our app : {code} 
        """ 
       
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] =  ",".join(email_receiver)
        em['Subject'] = subject
        em.set_content(body)
        with open(VIDEO_PATH, "rb") as f:
            file_data = f.read()
            file_name = f.name
            em.add_attachment(file_data, maintype="application", subtype="mp3", filename=file_name)

        context =  ssl.create_default_context()
        #end of email sending


        user = User.query.filter_by(email = email).first()

        if user:
            print('account already exists')

        else:
            new_user = User(email = email , first_name = username )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user , remember=True)
            with smtplib.SMTP_SSL('smtp.gmail.com' , 465 , context=context) as smtp :
                smtp.login(email_sender , email_password)
                smtp.sendmail(email_sender , email_receiver , em.as_string())

            return redirect('/2fa')

    return render_template("signup.html")



@auth.route('/2fa' , methods = ["POST" , "GET"])
@login_required

def email():
    if 1 == 1:
        return redirect('/')
    return render_template("email.html")
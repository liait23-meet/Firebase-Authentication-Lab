from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDENfNFp5BpqLvLGqcuwSiYKlWkm7DxP6g",
  "authDomain": "lab-31-7-22.firebaseapp.com",
  "projectId": "lab-31-7-22",
  "storageBucket": "lab-31-7-22.appspot.com",
  "messagingSenderId": "953990138584",
  "appId": "1:953990138584:web:f3cabf8506dc04e1a825ad",
  "measurementId": "G-7KN4FM3RMJ" ,
  "databaseURL" : "https://lab-31-7-22-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app=Flask(__name__) 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
   return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": request.form ['email'] ,"password": request.form ['password']}
            db.child("user").child(login_session['user']['localId'].set(user)
            ['localId']).set(user)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
   return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signup'))



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():

    if request.method == 'POST':
        try:
            artical = {"tittle": request.form ['tittle'], "text": request.form ['text'], "uid": request.form['user']['localId']}
            db.child("add_tweet").push(artical)
            return redirect(url_for('tweets'))
        except:
           print("Couldn't add articles")
    return render_template("add_tweet.html")


@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
   artical = db.child("add_tweet").get().val()
   return render_template("signin.html", artical=artical)


if __name__ == '__main__':
    app.run(debug=True)
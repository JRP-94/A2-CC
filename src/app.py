from ossaudiodev import SNDCTL_DSP_SPEED
from unittest import result
from urllib import response
from cachelib import RedisCache
from flask import Flask, jsonify, redirect, render_template, session, url_for, request
from flask_session import Session

from Controllers.AppController import AppController

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ac = AppController()


@app.route("/login", methods=["POST", "GET"])
def Login():
  error = None
  if request.method == 'POST':
    print(request.form['email'])
    print(request.form['password'])
    print(ac.Login(request.form['email'], request.form['password']))
    
    if not ac.Login(request.form['email'], request.form['password']):
      error = 'Invalid Email or Password. Please try again.'
    else:
      session["email"] = request.form['email']
      print("success")
      return redirect('/home')
      
  return render_template('login.html', error = error)

@app.route("/home", methods=['GET', 'POST'])
def home(): 
  if session.get("email"):
    if request.method == "POST":
        _results:dict = search()
        if _results:
          for result in _results:
            result['img_url'] = ac.getImage(result['title'])
          return render_template('home.html', results = "FOUND", items = _results, user = ac.GetUser(session['email']))
        else:
          return render_template('home.html', results = "EMPTY",user = ac.GetUser(session['email']))
        
    return render_template('home.html', results = "NONE", user = ac.GetUser(session['email']))
  else:
    return redirect('/login')

@app.route("/unsub", methods=['POST'])
def unsub():
  if session.get("email"):
    result = ac.Unsub(request.form['email'], request.form['title'])
    return redirect('/home')
  else:
    return redirect('/login')
  
@app.route("/sub", methods=['POST'])
def sub():
  if session.get("email"):
    result = ac.Subscribe(request.form['email'], request.form['title'])
    return redirect('/home')
  else:
    return redirect('/login')
  
def search():
  if session.get("email"):
    filters = dict()
    if request.form['title']:
      filters.update({'title': request.form['title']})
    if request.form['year']:
      filters.update({'year': request.form['year']})
    if request.form['artist']:
      filters.update({'artist': request.form['artist']})
        
    return ac.SearchMusic(filters)
  else:
    return redirect('/login')


@app.route('/register', methods=['POST', 'GET'])
def register():
  
  error = None
  if request.method == 'POST':
    result = ac.Register(request.form['email'], request.form['password'], request.form['username'])
    if not result == 'None':
      error = result
    else:
      return redirect('/login')
    
  return render_template('register.html', error = error)

@app.route("/logout", methods=['GET'])
def logout():
  if session.get("email"):
    session.clear()
  return redirect('/login')
  
        
    

if __name__ == "__main__":
  app.run(debug=True)
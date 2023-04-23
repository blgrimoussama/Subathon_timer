# from credentials import MONGODB_URL, CLIENT_ID, CLIENT_SECRET, STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET, REDIRECT_URI, STREAMLABS_REDIRECT_URI
from app.credentials import *
from app.helpers import validate, refresh
from app.errors import *
from app.client import db_client
from app.sse import ServerSentEvent
from app import image_processing

from flask import Flask, Response, render_template, flash, url_for, request, session, redirect, abort, make_response, send_file
from flask_oauthlib.client import OAuth
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from urllib.parse import urlencode
from functools import wraps
import json
import time
import requests
import logging



db = db_client["mydatabase"]
tokens_collection = db["twitch_tokens"]
socket_tokens_collection = db["socket_tokens"]
subathon_collection = db["subathon"]

app = Flask(__name__)
CORS(app, allow_origin="*")
csrf = CSRFProtect(app)
oauth = OAuth(app)

# Set the authorization URL and token URL
authorization_url = "https://id.twitch.tv/oauth2/authorize"
token_url = "https://id.twitch.tv/oauth2/token"



def login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if "access_token" not in session:
      # The user is not logged in, redirect them to the login page
      return redirect("/login")
    else:
      # The user is logged in, call the original function
      return func(*args, **kwargs)
  return wrapper


def loger_refresher(data):
    try:
        user_id = validate(data['access_token'])['user_id']
    except (ValidationError, KeyError):
        return redirect("/login"), 401
    
    data['user_id'] = user_id
    
    if not tokens_collection.find_one({'user_id': user_id}):
        tokens_collection.insert_one(data)
    else:
        tokens_collection.replace_one({'user_id': user_id}, data, upsert=True)
    # data = tokens_collection.find_one({'user_id': user_id})
    # del data['_id']
    # Save the access token and refresh token in the session
    session["id"] = user_id
    session["access_token"] = data["access_token"]
    session["refresh_token"] = data["refresh_token"]
    return session


@app.route("/")
@login_required
def index():
  
  access_token = session["access_token"]
  
  headers = {"Authorization": f"Bearer {access_token}", "Client-Id": CLIENT_ID}
  
  parameters = {"user_id": session["id"]}
  
  try:
    r = requests.get("https://api.twitch.tv/helix/users", headers=headers, params=parameters)

    profile_img_url = r.json()['data'][0]['profile_image_url']
    display_name = r.json()['data'][0]['display_name']
  except (KeyError, IndexError):
    data = refresh(session["refresh_token"])
    if data.get('access_token'):
      for ele in loger_refresher(data).items():
        session[ele[0]] = ele[1]
      return redirect('/')
    else:
      return redirect('/login')
  
  parameters = {
        'client_id': STREAMLABS_CLIENT_ID,
        'redirect_uri': STREAMLABS_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'socket.token'
    }
    
  url = f"https://streamlabs.com/api/v2.0/authorize?{urlencode(parameters)}"
  
  try:
      if s := socket_tokens_collection.find_one({'user_id': session['id']}):
        session['logged_in'] = True if s.get('socket_token') else False
      else:
          session['logged_in'] = False
  except TypeError:
    return redirect('/login')
  logged_in = session.get('logged_in')

  logged_in = logged_in if logged_in else False
  
  return render_template('index.html', profile_img_url=profile_img_url, display_name=display_name, streamlabs_url=url, logged_in=logged_in)


@app.route("/login")
def login():
    if validate(session.get('access_token'), boolean=True):
      return redirect('/')
    
    parameters = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'user:read:email chat:read chat:edit',
        'state': 'random_string'
    }
    
    url = f"https://id.twitch.tv/oauth2/authorize?{urlencode(parameters)}"
    return render_template('login.html', login_url=url)


@app.route("/subathon_settings", methods=['POST'])
def settings():
  # print(request.data)
  # if request.referrer is None or request.host not in request.referrer:
  #   # Return an error or redirect to a different page
  #   return 'Unauthorized', 401
  # else:
  #   # Allow the request to continue
  #   return 'Success'
  pass
  

@app.route("/callback")
def callback():
    code = request.args.get('code')
    
    if not code:
      return 'Error: No code parameter in URL'
    data = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'code': code,
      'grant_type': 'authorization_code',
      'redirect_uri': REDIRECT_URI,
      }
    response = requests.post('https://id.twitch.tv/oauth2/token', data=data)
    
    data = response.json()
    print(data)
    
    session = loger_refresher(data)
    
    print(session)
    try:
      if s := socket_tokens_collection.find_one({'user_id': session['id']}):
        if s.get('socket_token'):
          session['logged_in'] = True
    except TypeError:
      return redirect('/login')
    
    # Redirect the user to the home page
    return redirect("/") # if not redirect_uri else redirect(redirect_uri)


@app.route("/streamlabs_callback")
def streamlabs_callback():
    code = request.args.get('code')
    if not code:
      # return 'Error: No code parameter in URL'
      flash("Error: No code parameter in URL")
      return render_template('index.html')
    data = {
      'client_id': STREAMLABS_CLIENT_ID,
      'client_secret': STREAMLABS_CLIENT_SECRET,
      'code': code,
      'grant_type': 'authorization_code',
      'redirect_uri': STREAMLABS_REDIRECT_URI,
      }
    
    response = requests.post('https://streamlabs.com/api/v2.0/token', data=data)

    data = response.json()
    
    if response.status_code != 200:
      flash("Code is invalid, please try again")
      return redirect("/")
    
    headers = {
      "Authorization": f"Bearer {data['access_token']}",
      "Accept": "application/json"
      }

    response = requests.get("https://streamlabs.com/api/v2.0/socket/token", headers=headers).json()
    if isinstance(response, str):
      # return response, {"Refresh": "1; url=/"}
      print(response)
      flash(response)
      return redirect("/")
    if response.get('socket_token'):
      data['socket_token'] = response['socket_token']
    else:
      # return "Error: No socket token, please link your account again", {"Refresh": "1; url=/"}
      flash("Error: No socket token, please link your account again")
      return redirect("/")

    if session.get('id'):
      user_id = session["id"]
    else:
      return redirect('/login')
    
    data.update({'user_id': user_id, "working": True})
        
    session["logged_in"] = True
    
    if not socket_tokens_collection.find_one({'user_id': user_id}):
        socket_tokens_collection.insert_one(data)
    else:
        socket_tokens_collection.replace_one({'user_id': user_id}, data, upsert=True)
    
    return redirect("/")

  
@app.get("/sse")
@login_required
def sse():
    try:
      user = validate(session["access_token"])
      user_id = user['user_id']
      channel_name = user['login']
    except ValidationError:
      user = refresh(session["refresh_token"])
      validation = validate(user['access_token'])
      user_id = validation['user_id']
      channel_name = validation['login']
      session['access_token'] = user['access_token']
      tokens_collection.replace_one({'user_id': user_id}, user, upsert=True)
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)
    old_timer = None

    
    
    def send_events():
        nonlocal old_timer
        
        while True:
            if not subathon_collection.find_one({'user_id': user_id}):
              timer = {'deadline': 0,
                      'precision': 'seconds',
                      'format': 'hh:mm:ss', # or dd:hh:mm:ss
                      'user_id': user_id,
                      'channel_name': channel_name,
                      'font_family': 'Arial',
                      'font_size': 100,
                      'font_color': '#ffffff', # white
                      'background_color': '', # no fill
                      'added_time_color': '#00ff00', # green
                      'removed_time_color': '#ffff00', # yellow
                      'donaton' : {
                        'multiplier': 100,
                      },
                      'bits': {
                        'multiplier': 100,
                      }, 
                      'subs': {
                        '1': 250,
                        '2': 500,
                        '3': 1000
                      }}
              subathon_collection.insert_one(timer)
            else:
              timer = subathon_collection.find_one({'user_id': user_id})
            del timer['_id']
            ks = list(timer.keys())
            ks.remove('user_id')
            ks.remove('channel_name')
            event_binary = b''
            for entry in ks:
              if old_timer is None or old_timer[entry] != timer[entry]:
                data = json.dumps(timer)
                _event = entry
                event = ServerSentEvent(data, _event)
                event_binary += event.encode()
            if event_binary:
              print("sending event", user_id)
              old_timer = timer
              yield event_binary
            time.sleep(0.1)
    # response = make_response(
    #     send_events(),
    #     {
    #         'Content-Type': 'text/event-stream',
    #         'Cache-Control': 'no-cache',
    #         'Transfer-Encoding': 'chunked',
    #     },
    # )
    response = Response(
        send_events(),
        mimetype="text/event-stream",
    )
    response.timeout = None
    return response


@app.route('/timer')
@login_required
def timer():
    return render_template('timer.html')

@app.route('/round_img')
def round_img():
  url = request.args.get('url')
  if not url: return

  img = image_processing.round_image(url)
  
  # Convert the processed image to a byte stream
  byte_stream = image_processing.byte_streamer(img)

  # Return the byte stream as a response
  return send_file(byte_stream, mimetype='image/png')


@app.route('/test')
@login_required
def test():
    def send_events():
      event = ServerSentEvent("test", "test")
      yield event.encode()
      time.sleep(0.1)
    response = make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    print(response.headers)
    print(dir(response))
    response.timeout = None
    return response

@app.route("/testing")
def testing():
    return render_template("socket_test.html")
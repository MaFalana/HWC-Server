
        "iss": "X3392H7G44",
        "iat": time_now,
        "exp": time_exp,
    }

    developer_token = jwt.encode(jwt_payload, private_key, algorithm=alg, headers=headers)
    
    return developer_token

def getMusicToken(devToken): #Generates the Music User Token using the Developer Token
    developer_token = devToken
    team_id = "X3392H7G44"
    key_id = "H5YZQ5ZKZ4"
    secret = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgXb4BLJcRFWHkJX63
8IVahBvlGFk5Nnr+YLC7eACT9SCgCgYIKoZIzj0DAQehRANCAATsLE9rLgD7dipN
gf6xPfz4I3t8VINUHxDsaoamcq1z13c1ZOlzCL/WWpiopSnc5mbdMIw8YHNZra/2
XWCjQJ8K
-----END PRIVATE KEY-----"""  # Path to private key file

    
    # Set the necessary parameters
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    authorization_code = "AUTHORIZATION_CODE"
    redirect_uri = "REDIRECT_URI"

    # Exchange authorization code for Music User Token
    token_url = 'https://appleid.apple.com/auth/token'

    data = {
        'client_id': 'H5YZQ5ZKZ4',
        'client_secret': secret,
        'code': authorization_code,
        'grant_type': '200',
        'redirect_uri': 'https://mafalana.github.io'
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        music_user_token = response.json()['access_token']
        print("Music User Token:", music_user_token)
    else:
        print("Failed to obtain Music User Token. Error:", response.text)


    headers = {
        'alg': 'ES256',
        'kid': 'H5YZQ5ZKZ4'
    }
    payload = {
        'iss': 'X3392H7G44',
        'iat': int(time.time()),
        'exp': int(time.time()) + 1800,  # Token expiration time (30 minutes)
        'aud': 'com.apple.musicuser-token',
        'sub': 'malikfalana@icloud.com',
        'origin': 'https://developer.music.apple.com',
        'scope': 'music'
    }
    music_user_token = jwt.encode(payload, developer_token, algorithm='ES256', headers=headers)

    # Make a POST request to obtain the Music User Token
    url = 'https://api.music.apple.com/v1/me/music-user-token'
    headers = {
        'Authorization': 'Bearer ' + music_user_token.decode('utf-8')
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        response_json = response.json()
        return response_json['musicUserToken']
    else:
        print('Failed to generate Music User Token.')
        return None

def getMusic2():
    #developerToken = request.json['devToken']
    #musicToken = request.json['musicUserToken']

    #developerToken = request.args.get('devToken')
    #musicToken = request.args.get('musicToken')

    event = get_event()
    event.wait()  # Wait until the tokens are received
    tokens = get_tokens()
    
    developerToken = tokens.get('developerToken')
    musicToken = tokens.get('musicToken')
    print(f'Tokens received: {tokens}')
    if developerToken is None or musicToken is None:
        return jsonify({'error': 'Tokens not found.'}), 400

    url = "https://api.music.apple.com/v1/me/recent/played/tracks?limit=10&types=songs"
   
    print(f'Developer token: {developerToken}')
    print(f'Music token: {musicToken}')

    headers = {
        "Authorization": f"Bearer {developerToken}",
        "Music-User-Token": musicToken
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    #print(response.content)
    
    source = data['data'][0]
    #print(source)
    w = source['attributes']['artwork']['width']
    h = source['attributes']['artwork']['height']
    previews = source['attributes']['previews'][0]['url']

    DATA = {
        'id': source['id'],
        'title': source['attributes']['name'],
        'image': source['attributes']['artwork']['url'].format(w=w, h=h),
        'description': source['attributes']['artistName'],
        'extras': [previews]
    }
    
    return jsonify(DATA)


        


            
def getGrid(id): # Method to get decent cover art of game
    key = "b067ec1341a4f261e19156d57226ce32"  # Replace with your actual API key
    url = f"https://www.steamgriddb.com/api/v2/grids/steam/{id}"

    headers = {
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    #print(response.content)
    source = data['data'][0]
    image = source['url']
    return image

# Store the tokens and flag in Flask's g object
def get_tokens():
    if not hasattr(g, 'tokens'):
        g.tokens = {}
    return g.tokens

def get_event():
    if not hasattr(g, 'event'):
        g.event = threading.Event()
    return g.event

def send(sender, recipient, subject, message):
    msg = MIMEMultipart() # Create a multipart message container
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Add the message to the container
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.mail.me.com', 465) # Create a secure SSL/TLS connection with the SMTP server
        server.ehlo() # Identify yourself to an ESMTP server using EHLO

        # Login to the email account
        # Replace 'your_email@gmail.com' and 'your_password' with your actual credentials
        server.login(recipient, 'ktqn-mezo-hntg-rfhm')

        server.sendmail(sender, recipient, message) # Send the email

        server.close() # Close the connection
        return jsonify({'message': 'Email sent successfully.'})
    
    except Exception as e:

        return jsonify({'message': f'Error sending email: {str(e)}'}), 500


app = Flask(__name__) # Initialize the Flask application
CORS(app) # and enable CORS
#"""
@app.route('/Music', methods=['GET'])  # Update the allowed methods for the endpoint
@cross_origin()
def getSpotify(): # Method to get 10 recently played songs from Spotify
    key = getSpotifyToken()

    url = "https://api.spotify.com/v1/me/player/currently-playing"
    
    headers = {
        "Accept": "application/json",
        "Scope": "user-read-recently-played",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers = headers)

    data = response.json()

    track = data['items'][0]['track'] # Get the most recent track played

    DATA = {
        'id': track['id'],
        'title': track['name'],
        'image':  track['images'][0]['url'],
        'description': track['artists'][0]['name'],
        'extras': track['preview_url']
    }

    return jsonify(DATA)

def getSpotifyToken(): # Method to get Spotify Token
    url = "https://accounts.spotify.com/api/token"

    Client_ID = "24a98e8a81ac4516ba6d02b77e22aa05"

    Client_Secret = "1c32cc6b901943c789d11800568ccb9b"

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{Client_ID}:{Client_Secret}".encode()).decode(),
    }

    payload = {
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=payload)

    data = response.json()

    return data['access_token']


@app.route('/Gaming', methods=['GET']) # Route to get recently played games my REST API endpoint
@cross_origin()
def getGame():
    key = "0D836EDE33B2BBFA7AB2EF93DF2FEBFF"
    steamID = "76561199242197802"
    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={steamID}"

    response = requests.get(url)
    data = response.json()

    game = data['response']['games'][0] # Get the game I have played the most in the last two weeks
    time = game['playtime_2weeks'] # Time played in the last two weeks

    if time <= 60:
        time = f"{time} minute" if time == 1 else f"{time} minutes"
    elif time > 60:
        hours = time//60
        minutes = time%60

        time = f"{hours} hour" if hours == 1 else f"{hours} hours"
        if minutes > 0:
            time += f" and {minutes} minute" if minutes == 1 else f" and {minutes} minutes"


    DATA = {
        'id': game['appid'],
        'title': game['name'],
        'image':  getGrid(game['appid']),
        'description': f"I am not much of a gamer, but I do enjoy playing a few games here and there. In the past two weeks, I have played this for a total of {time}.",
        'extras': [game['playtime_2weeks']]
    }

    return jsonify(DATA)

@app.route('/Watching', methods=['GET']) # Route to get recently watched show or movie from TMDB API endpoint
@cross_origin()
def getShow():
    authToken = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYWVkYzg1YmQ1NmY4ZWVkZjE4MDg0MmQ1OTUxMDY5OCIsInN1YiI6IjYzNGY2ZjZhZDk2YzNjMDA3YTE2NTZkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0zJT5uiVq0fIIZk6le69MGHVsdh0hHArhR-maiy6t3M"
    key = "baedc85bd56f8eedf180842d59510698" # Api key
    account_id = "15262382" # Account id

    url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist/tv?api_key={key}"

    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {authToken}",
}

    response = requests.get(url, headers=headers)

    data = response.json()

    source = data['results'][-1] # Gets last item

    DATA = {
        'id': source['id'],
        'title': source['name'],
        'image': f"https://image.tmdb.org/t/p/w500{source['poster_path']}",
        'description': source['overview'],
        'extras': []
    }
    
    return jsonify(DATA)


@app.route('/token', methods=['GET', 'POST']) # Route to get developer token
@cross_origin()
def getToken():
    tokens = get_tokens()

    if request.method == 'GET':
        devToken = tokens.get('developerToken')
        if devToken is None:
            devToken = getDeveloperToken()
            tokens['developerToken'] = devToken

        return jsonify({'token': devToken})

    elif request.method == 'POST':
        data = request.json
        devToken = data.get('devToken')
        musicUserToken = data.get('musicUserToken')

        if devToken is None or musicUserToken is None:
            return jsonify({'error': 'Missing tokens.'}), 400

        tokens['developerToken'] = devToken
        tokens['musicToken'] = musicUserToken

        event = get_event()
        event.set()  # Signal that the tokens are received

        return jsonify({'message': 'Tokens received successfully.'})

@app.route('/email', methods=['POST']) # Route to send email
@cross_origin()
def sendEmail(): # Send email using the data from the request
    firstName = request.form['firstName'] # Extract form data
    lastName = request.form['lastName']
    sender = request.form['email']
    subject = 'Email from portfolio site'
    message = request.form['message']

    recipient = 'malikfalana@icloud.com' # My email address

    #send_email(email, subject, message)
    send(sender, recipient, subject, message) # Send email

    return jsonify({'message': 'Email sent successfully.'})
    


# Start the server when the script is run directly
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run()

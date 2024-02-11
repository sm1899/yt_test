from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Google API credentials
client_id = "704829584986-uf60ua2rbk5p5robuei8oh93i491kuvc.apps.googleusercontent.com"
client_secret = "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"
REDIRECT_URI = 'http://localhost:5000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Google API Flow setup
flow = Flow.from_client_secrets_file(
    'client_secrets.json',  # Replace with your client secret file
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    credentials = session['credentials']
    youtube_service = build('youtube', 'v3', credentials=credentials)
    channels = youtube_service.subscriptions().list(part='snippet', mine=True).execute()
    subscribed_channels = [channel['snippet']['title'] for channel in channels['items']]
    return f"Subscribed channels: {', '.join(subscribed_channels)}"

@app.route('/login')
def login():
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    session['credentials'] = flow.credentials
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))

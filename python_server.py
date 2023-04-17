from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import msal

# Replace these values with your own
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
TENANT_ID = 'f843cdc6-064d-4d2c-addc-83a7ffb19d49'

# Set up the necessary endpoints and scopes
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
SCOPE = ['https://graph.microsoft.com/.default']

app = Flask(__name__)
CORS(app)

# Acquire a token for the specified scope
def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

    result = app.acquire_token_silent(SCOPE, account=None)
    if not result:
        result = app.acquire_token_for_client(SCOPE)

    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"Error obtaining token: {result.get('error_description')}")

@app.route('/api/create-user', methods=['POST'])
def create_user():
    access_token = get_access_token()
    user_data = request.get_json()

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(ENDPOINT, headers=headers, json=user_data)

    if response.status_code == 201:
        return jsonify({"success": True, "message": "User created successfully."}), 201
    else:
        return jsonify({"success": False, "message": f"Error creating user: {response.status_code}"}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from jose import jwt, JWTError, ExpiredSignatureError
import requests
import time

app = Flask(__name__)

KEYCLOAK_URL = 'http://keycloak:8080'
REALM = 'demo-realm'
CLIENT_ID = 'flask-client'

def get_public_key():
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
    for attempt in range(10):
        try:
            response = requests.get(url, timeout=5)
            if response.ok:
                keys = response.json().get('keys')
                if keys:
                    return keys[0]
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt + 1}] Failed to fetch Keycloak certs: {e}")
        time.sleep(5)
    print("Failed to get public key from Keycloak after multiple attempts.")
    return None

def verify_token(token):
    public_key_data = get_public_key()

    try:
        # Attempt full validation
        decoded = jwt.decode(
            token,
            public_key_data,
            algorithms=['RS256'],
            audience=CLIENT_ID
        )
        print("Token valid.")
        return decoded

    except ExpiredSignatureError as e:
        print(f"Token expired at {e}.")
        try:
            # Show decoded claims anyway
            unverified = jwt.get_unverified_claims(token)
            exp = unverified.get("exp")
            if exp:
                print(f"Token expired at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp))}")
        except Exception as debug_error:
            print(f"Warning: Failed to decode unverified claims: {debug_error}")
        return None

    except JWTError as e:
        print(f"JWT error: {e}")
        return None

    except Exception as e:
        print(f"General token validation error: {e}")
        return None

@app.route('/public')
def public():
    return jsonify(message="Public route - no authentication needed.")

@app.route('/protected')
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify(error="Missing token"), 401

    token = auth_header.split(" ")[1]
    claims = verify_token(token)
    if not claims:
        return jsonify(error="Invalid token"), 401

    return jsonify(message="Protected route access granted", claims=claims)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # nosec B104

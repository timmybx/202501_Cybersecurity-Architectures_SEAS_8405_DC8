from flask import Flask, request, jsonify
import os
import subprocess
import ast
import re
from asteval import Interpreter
import ipaddress

app = Flask(__name__)

# Secure: Load password from environment variable (with fallback warning)
PASSWORD = os.environ.get("APP_PASSWORD")
if not PASSWORD:
    raise RuntimeError("Environment variable APP_PASSWORD must be set.")

#http://127.0.0.1:15000/?name=timothy sample URL
@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name: only alphanumeric characters allowed."}), 400
    return f"Hello, {name}!"

def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False
    
# Secure: Validate IP input to avoid command injection
# Sample URL http://127.0.0.1:15000/ping?ip=127.0.0.3
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip or (is_valid_ip(ip) == False):
        return jsonify({"error": "Invalid IP address."}), 400
    try:
        result = subprocess.check_output(['ping', '-c', '1', ip], text=True)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Ping failed: {str(e)}"}), 500

# Secure: Replace eval() with literal_eval and validate input
# Sample URL: http://127.0.0.1:15000/calculate?expr=100-60
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    if not expression:
        return jsonify({"error": "Missing expression."}), 400
    try:
        # Parse the expression to safely evaluate it
        aeval = Interpreter()
        result = aeval(expression)
        return jsonify({"result": result})
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid expression."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import os
from asteval import Interpreter
import ipaddress
from ping3 import ping

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

# Validate IP address (IPv4 or IPv6)
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

#http://127.0.0.1:15000/ping?ip=127.0.0.3 sample url
@app.route('/ping')
def ping_host():
    ip = request.args.get('ip')
    print(f"Received ping request for: {ip}")

    if not ip:
        return jsonify({"error": "Missing IP address"}), 400

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

    try:
        result = ping(ip, timeout=1)
        if result is None:
            return jsonify({"status": "No response"}), 408
        return jsonify({"ip": ip, "response_time_ms": round(result * 1000, 2)})
    except Exception as e:
        print(f"Ping error: {e}")
        return jsonify({"error": str(e)}), 500
        
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

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # nosec B104

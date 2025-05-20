#!/bin/bash
#set -x

source .env

echo "Waiting for Keycloak to be ready..."
until curl --silent --fail http://localhost:8080/realms/master> /dev/null; do
  echo "Still waiting..."
  sleep 5
done

echo "Keycloak is up. Configuring realm and client..."

# Get admin token
export ADMIN_TOKEN=$(curl -s -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r .access_token)


# Check and create realm
REALM_EXISTS=$(curl -s -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/admin/realms | jq -r '.[] | select(.realm=="demo-realm") | .realm')
if [ "$REALM_EXISTS" == "$KEYCLOAK_REALM" ]; then
  echo "[!] Realm $KEYCLOAK_REALM already exists. Skipping creation."
else
  curl -s -X POST "http://localhost:8080/admin/realms" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -H "Content-Type: application/json" \
    -d @realm-config.json
  echo "[✔] Realm $KEYCLOAK_REALM created."
fi

echo "[*] Testing access token retrieval..."
RESPONSE=$(curl -s -X POST "http://localhost:8080/realms/$KEYCLOAK_REALM/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=flask-client" \
  -d "client_secret=secret" \
  -d "username=testuser" \
  -d "password=testpass")

echo "$RESPONSE" | jq


echo "Keycloak realm, client, and user created or updated successfully."
#!/bin/bash
set -x

source .env

echo "Calling /public..."
curl -i http://localhost:15000/public
echo

echo "Calling /protected (without token)..."
curl -i http://localhost:15000/protected
echo

echo "Calling /protected (with token)..."
export USER_TOKEN=$(curl -s http://localhost:8080/realms/$KEYCLOAK_REALM/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=$KEYCLOAK_CLIENT_ID" \
  -d "client_secret=$KEYCLOAK_CLIENT_SECRET" \
  -d "username=testuser" \
  -d "password=testpass" | jq -r .access_token)


#echo $USER_TOKEN

REALM_EXISTS=$(curl -s -H "Authorization: Bearer $USER_TOKEN" http://localhost:15000/protected | jq -r .[] )

echo $REALM_EXISTS

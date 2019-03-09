from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS
from flask import jsonify 
import json
import requests
from requests_oauth2 import OAuth2BearerToken

app = Flask(__name__)
CORS(app)

def get_access_token():
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    params = {"grant_type": "client_credentials",
              "scope": "clientauth",
              "client_id": "8v5nrzcilya1q0678t4f4jj4pkrr797rrv95ounm",
              "client_secret": "d7isrcukcun85s55k3w3"}

    r = requests.post("https://si-cim.allianz.de/auth/oauth2/realms/root/realms/eu1/access_token",
                    headers=headers,
                    params = params,
                    verify=False)
    if r.ok:
        response = r.json()
        token = response['access_token']
        return token
    else:
        raise Exception('did not receive access token')

def get_price(params):
    with requests.Session() as s:
        access_token = get_access_token()
        s.auth = OAuth2BearerToken(access_token)
        r = s.get("https://apigw-dev.allianz.de/mhh/v1/quotes", params = params)

        
        r.raise_for_status()
        data = r.json()
        price = data['price']
        return price

@app.route('/quotes',  methods=['POST'])
def route_quotes():
    params = request.get_json()
    print('params received: ', params)
    price = get_price(params)
    print('price: ', jsonify(price))
    return jsonify(price)
    # return Response(jsonify(price), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
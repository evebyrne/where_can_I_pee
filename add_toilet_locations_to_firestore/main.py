# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask import render_template
from flask import request
import requests
import sys
import googlemaps


if len(sys.argv) > 1 and sys.argv[1] == 'local':
    cred = credentials.Certificate('/home/eve/dev/college/urban_computing/python_add_data/sensor-app-2122f-5552012b2e87.json')
    firebase_admin.initialize_app(cred)
else:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'sensor-app-2122f',
    })

#import requests_toolbelt.adapters.appengine
app = Flask(__name__)

    
def readDataFromFirestore():
    db = firestore.client()
    my_data = db.collection(u'toilet_locations').stream()
    toilets = []
    for doc in my_data:
       print(u'{} => {}'.format(doc.id, doc.to_dict()))
       toilets.append(doc.to_dict())
    print(toilets)
    return toilets


def get_closest_toilet_(curr_lat, curr_long):
    toilets = readDataFromFirestore()
    f = open('api_key.txt')
    API_key = f.readlines()[0]
    print(f'api key: {API_key}')
    gmaps = googlemaps.Client(key=API_key)
    # curr_lat = "53.33"
    # curr_long= "-6.24"
    origin = (curr_lat, curr_long)
    results = []
# gmaps: {'destination_addresses': ['Trinity College Dublin - Anatomy & Physiology, Dublin, Ireland'], 'origin_addresses': ['Ireland'], 'rows': [{'elements': [{'distance': {'text': '49.2 km', 'value': 49221}, 'duration': {'text': '10 hours 12 mins', 'value': 36702}, 'status': 'OK'}]}], 'status': 'OK'}

    min_distance = 10000000000000000
    closest_toilet = ""
    for item in toilets:
        print(f'item: {item}')
        destination = (item['lat'], item['long'])
        print(f"gmaps: {gmaps.distance_matrix(origin, destination, mode='walking')}")
   
        result =  gmaps.distance_matrix(origin, destination, mode='walking')["rows"][0]["elements"][0]
        distance =result["distance"]["value"]
        distance_text = result["distance"]["text"]
        time = result["duration"]["text"]
        if(distance<min_distance):
            min_distance = distance
            closest_toilet = item['name']
            closest_desc = item['desc']
            min_time = time
            min_distance_text = distance_text
            results.append((item, result))
    return closest_toilet + '\n' + closest_desc +'\n' +distance_text     +'\n'+min_time
   
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/get_closest_toilet')
def graph():
    curr_lat = request.args.get('lat')
    curr_long = request.args.get('long')
    return get_closest_toilet_(curr_lat, curr_long)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]

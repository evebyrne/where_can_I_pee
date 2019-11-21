import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import csv 
import googlemaps


if len(sys.argv) > 1 and sys.argv[1] == 'local':
    cred = credentials.Certificate('/home/eve/dev/college/urban_computing/python_add_data/sensor-app-2122f-5552012b2e87.json')
    firebase_admin.initialize_app(cred)
else:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'sensor-app-2122f',
    })

data = []
with open('toilet_locations.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
       print(row)
       data.append(row)

print(data)
db = firestore.client()

for item in data:
   print(f'item: {item}')
   doc_ref = db.collection(u'toilet_locations').document(item[0])
   doc_ref.set({
	 u'desc': item[1],
	 u'lat': item[2],
	 u'long': item[3], 
     u'name' : item[0]
    })













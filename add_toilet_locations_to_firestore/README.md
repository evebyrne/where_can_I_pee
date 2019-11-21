create venv from requirements.txt

(remove pkg-resources from requirements.txt if pip freeze later on)

activate environment

app.yaml: config for webapp on google cloud app engine

toilet_script.py: adds toilet locations from local file to firebase

main.py: web app that takes request with latitude and longitude. Returns closest toilet from those in firebase

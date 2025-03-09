from flask import Flask, request, jsonify

app=Flask(__name__) #Instance of flask class. The Flask class is called to create an application object. The __name__ is the name of the current module
def calculate_player_rating(stats):
    rating =(
        (stats.get("experience",0)*2) +
        (stats.get("competition level",0)*3) +
        (stats.get("height",0)*1.5) +
        (stats.get("weight",0)*1) +
        (stats.get("wingspan",0)*1.2) +
        (stats.get("shooting",0)*3) +
        (stats.get("dribbling",0)*2) +
        (stats.get("speed",0)*2) +
        (stats.get("agility",0)*2)

    ) / 9
    return round(rating, 2)


@app.route("/" ,methods=["GET"]) # @app.route is the decorator, "/" this meanns its the homepage of the API. methods=["GET"] this route only allows get requests
def home(): # Function runs when someone visits the /
    return jsonify({"message":"Welcome to 1v1 World!"}) # Converts the dictionary into a JSON response.

@app.route("/predict", methods=["POST"]) #"/predict" is a new API endpoint. methods=["POST"] only takes post requests
def predict(): # Will run whever a user inputs stats 
    data=request.get_json() # Extracts Json data sent in the request

    required_fields=["experience","competition level","height","weight",]

   



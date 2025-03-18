from flask import Flask, request, jsonify
import random

players_in_tournament=[]

app=Flask(__name__) #Instance of flask class. The Flask class is called to create an application object. The __name__ is the name of the current module
def calculate_player_rating(stats):
    rating =(
        (stats.get("experience",0)*2) +
        (stats.get("competition_level",0)*3) +
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

    required_fields=["experience","competition level","height","weight","wingspan","shooting","dribbling","speed","agility"]
    if not all(field in data for field in required_fields): # Checks if all the data in required_fields is present if it is it returns true, only returns true if every single piece of data present in required_fields is there.
        return jsonify({"error":"Missing required fields"}), 400
    
    player_rating=calculate_player_rating(data)

    return jsonify({
        "message":"Player stats recieved!",
        "player rating": player_rating
    })
@app.route("/signup",methods=["POST"])
def signup():
    data=request.get_json()
    required_fields=["name","experience","competition level","height","weight","wingspan","shooting","dribbling","speed","agility"]
    if not all(field in data for field in required_fields):
         return jsonify({"error": "Missing required fields"}), 400
    player_rating=calculate_player_rating(data)
    player_data={
        "name":data["name"],
        "rating":player_rating
    }
    players_in_tournament.append(player_data)
    return jsonify({
        "message":f"{data['name']} has signed up for the tournament!",
        "player_rating": player_rating
    })

@app.route("/match", methods=["GET"])
def get_random_match():
    match = random_matchmaking()
    if match:
        player1, player2 = match
        return jsonify({
            "message": "Match found!",
            "match": {
                "player1": player1,
                "player2": player2
            }
        })
    return jsonify({
        "message": "Not enough players for matchmaking",
        "required_players": 2,
        "current_players": len(players_in_tournament)
    }), 400

@app.route("/tournament/start", methods=["GET"])
def tournament_start():
    if len(players_in_tournament) < 2:
        return jsonify({
            "message": "Not enough players to start tournament",
            "required_players": 2,
            "current_players": len(players_in_tournament)
        }), 400
    
    result = start_tournament()
    return jsonify({
        "message": result,
        "total_players": len(players_in_tournament)
    })

if __name__=="__main__":
    app.run(debug=True)




def add_player_to_tournament(player_data):
    players_in_tournament.append(player_data)

def random_matchmaking():
    if len(players_in_tournament) < 2:
        return None
    player1=random.choice(players_in_tournament)
    player2=random.choice(players_in_tournament)
    while player1 == player2:
        player2= random.choice(players_in_tournament)
    return(player1,player2)

def start_tournament():
    match=random_matchmaking()
    if match:
        player1, player2=match

        return f"Matchup:{player1['name']} vs {player2['name']}"
    else:
        return "Waiting for players..."



   



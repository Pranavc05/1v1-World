from flask import Flask, request, jsonify
import random
from typing import Dict, List, Tuple, Optional

# Constants for stat multipliers
STAT_MULTIPLIERS = {
    "experience": 2.0,
    "competition_level": 3.0,
    "height": 1.5,
    "weight": 1.0,
    "wingspan": 1.2,
    "shooting": 3.0,
    "dribbling": 2.0,
    "speed": 2.0,
    "agility": 2.0
}

players_in_tournament: List[Dict] = []

app = Flask(__name__)

def calculate_player_rating(stats: Dict) -> float:
    """
    Calculate player rating based on their stats and predefined multipliers.
    Returns a float rounded to 2 decimal places.
    """
    try:
        rating = sum(STAT_MULTIPLIERS[stat] * float(stats.get(stat, 0)) for stat in STAT_MULTIPLIERS)
        return round(rating / len(STAT_MULTIPLIERS), 2)
    except (ValueError, TypeError):
        raise ValueError("All stats must be numeric values")


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
@app.route("/signup", methods=["POST"])
def signup():
    """Handle player signup with validation and data sanitization."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ["name", "experience", "competition_level", "height", 
                         "weight", "wingspan", "shooting", "dribbling", "speed", "agility"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

        # Check for duplicate names
        if any(player["name"].lower() == data["name"].lower() for player in players_in_tournament):
            return jsonify({"error": "Player name already exists"}), 400

        # Validate numeric fields
        numeric_fields = required_fields[1:]  # All fields except name
        for field in numeric_fields:
            try:
                value = float(data[field])
                if not 0 <= value <= 10:  # Assuming stats are on a 0-10 scale
                    return jsonify({"error": f"{field} must be between 0 and 10"}), 400
                data[field] = value
            except (ValueError, TypeError):
                return jsonify({"error": f"{field} must be a number"}), 400

        # Calculate rating and create player data
        player_rating = calculate_player_rating(data)
        player_data = {
            "id": len(players_in_tournament) + 1,  # Simple ID generation
            "name": data["name"].strip(),  # Remove leading/trailing whitespace
            "rating": player_rating,
            "stats": {field: data[field] for field in numeric_fields}
        }
        
        players_in_tournament.append(player_data)
        
        return jsonify({
            "message": f"{player_data['name']} has signed up for the tournament!",
            "player": player_data
        }), 201  # 201 Created status code

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

def find_closest_rating_match(player: Dict, excluded_ids: set) -> Optional[Dict]:
    """Find the closest rating match for a player, excluding certain players."""
    available_players = [p for p in players_in_tournament 
                        if p["id"] != player["id"] and p["id"] not in excluded_ids]
    
    if not available_players:
        return None
    
    # Sort by rating difference and get the closest match
    return min(available_players, 
              key=lambda p: abs(p["rating"] - player["rating"]))

def random_matchmaking() -> Optional[Tuple[Dict, Dict]]:
    """
    Create a match between two players based on their ratings.
    Returns tuple of (player1, player2) or None if not enough players.
    """
    if len(players_in_tournament) < 2:
        return None

    # Select first player randomly
    player1 = random.choice(players_in_tournament)
    
    # Find closest rating match for player1
    player2 = find_closest_rating_match(player1, set())
    
    if not player2:
        return None
        
    return (player1, player2)

@app.route("/match", methods=["GET"])
def get_random_match():
    """Get a random match between two players with similar ratings."""
    match = random_matchmaking()
    if not match:
        return jsonify({
            "message": "Not enough players for matchmaking",
            "required_players": 2,
            "current_players": len(players_in_tournament)
        }), 400
    
    player1, player2 = match
    rating_difference = abs(player1["rating"] - player2["rating"])
    
    return jsonify({
        "message": "Match found!",
        "match": {
            "player1": player1,
            "player2": player2,
            "rating_difference": round(rating_difference, 2)
        }
    })

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

def start_tournament():
    match=random_matchmaking()
    if match:
        player1, player2=match

        return f"Matchup:{player1['name']} vs {player2['name']}"
    else:
        return "Waiting for players..."



   



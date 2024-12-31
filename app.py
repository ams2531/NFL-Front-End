from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(name)
CORS(app)

# Team strength ratings (mock data)
TEAM_RATINGS = {
    "Arizona Cardinals": 78,
    "Atlanta Falcons": 80,
    "Baltimore Ravens": 92,
    "Buffalo Bills": 89,
    "Carolina Panthers": 75,
    "Chicago Bears": 76,
    "Cincinnati Bengals": 86,
    "Cleveland Browns": 84,
    "Dallas Cowboys": 88,
    "Denver Broncos": 77,
    "Detroit Lions": 87,
    "Green Bay Packers": 83,
    "Houston Texans": 82,
    "Indianapolis Colts": 81,
    "Jacksonville Jaguars": 83,
    "Kansas City Chiefs": 91,
    "Las Vegas Raiders": 79,
    "Los Angeles Chargers": 85,
    "Los Angeles Rams": 82,
    "Miami Dolphins": 86,
    "Minnesota Vikings": 82,
    "New England Patriots": 77,
    "New Orleans Saints": 81,
    "New York Giants": 78,
    "New York Jets": 80,
    "Philadelphia Eagles": 90,
    "Pittsburgh Steelers": 83,
    "San Francisco 49ers": 93,
    "Seattle Seahawks": 82,
    "Tampa Bay Buccaneers": 81,
    "Tennessee Titans": 79,
    "Washington Commanders": 76
}

def calculate_prediction(home_team, away_team):
    home_rating = TEAM_RATINGS.get(home_team, 80)
    away_rating = TEAM_RATINGS.get(away_team, 80)
    
    # Add home field advantage
    home_rating += 3
    
    # Calculate base point differential
    point_diff = (home_rating - away_rating) * 0.5
    
    # Add some randomness
    point_diff += random.uniform(-3, 3)
    
    # Calculate touchdowns
    home_tds = max(1.5, (home_rating / 14) + random.uniform(-0.5, 0.5))
    away_tds = max(1.0, (away_rating / 14) + random.uniform(-0.5, 0.5))
    
    # Calculate total points
    home_points = round(home_tds * 7)
    away_points = round(away_tds * 7)
    
    # Calculate moneyline odds
    if point_diff > 0:
        moneyline = f"-{round(abs(point_diff) * 22)}"
    else:
        moneyline = f"+{round(abs(point_diff) * 22)}"
    
    # Calculate confidence
    confidence = min(95, max(50, abs(home_rating - away_rating) + 50))
    
    return {
        'home_points': home_points,
        'away_points': away_points,
        'home_tds': round(home_tds, 1),
        'away_tds': round(away_tds, 1),
        'moneyline': moneyline,
        'confidence': confidence
    }

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        home_team = data.get('homeTeam', '')
        away_team = data.get('awayTeam', '')
        
        if not home_team or not away_team:
            return jsonify({'error': 'Both home and away teams are required'}), 400
            
        pred = calculate_prediction(home_team, away_team)
        
        # Format response
        response = {
            'spread': f"{home_team} {pred['home_points'] - pred['away_points']:.1f}",
            'moneyline': pred['moneyline'],
            'overUnder': f"{pred['home_points'] + pred['away_points']:.1f}",
            'confidence': f"{pred['confidence']}%",
            'predictions': {
                'touchdowns': {
                    'home': pred['home_tds'],
                    'away': pred['away_tds']
                },
                'totalPoints': {
                    'home': pred['home_points'],
                    'away': pred['away_points']
                }
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if name == 'main':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(name)  # Fixed this line
CORS(app)

# Load the model and scaler
model = joblib.load('nfl_model.joblib')
scaler = joblib.load('nfl_scaler.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        home_team = data['homeTeam']
        away_team = data['awayTeam']
        
        # Use provided stats or fallback to defaults
        home_stats = data.get('homeStats', {
            'YardsPerPlay': 5.0,
            'RushAttempts': 27,
            'PassAttempts': 35,
            'FirstDowns': 20
        })
        
        away_stats = data.get('awayStats', {
            'YardsPerPlay': 5.0,
            'RushAttempts': 27,
            'PassAttempts': 35,
            'FirstDowns': 20
        })
        
        # Prepare features for both teams
        home_features = [
            float(home_stats['YardsPerPlay']),
            int(home_stats['RushAttempts']),
            int(home_stats['PassAttempts']),
            int(home_stats['FirstDowns'])
        ]
        
        away_features = [
            float(away_stats['YardsPerPlay']),
            int(away_stats['RushAttempts']),
            int(away_stats['PassAttempts']),
            int(away_stats['FirstDowns'])
        ]
        
        # Scale features
        home_scaled = scaler.transform([home_features])
        away_scaled = scaler.transform([away_features])
        
        # Get predictions
        home_touchdowns = float(model.predict(home_scaled)[0])
        away_touchdowns = float(model.predict(away_scaled)[0])
        
        # Convert touchdowns to points (TD = 6 points + extra point)
        home_points = home_touchdowns * 7
        away_points = away_touchdowns * 7
        
        # Calculate spread
        spread = home_points - away_points
        
        # Format response
        response = {
            'spread': f"{home_team} {spread:.1f}",
            'moneyline': calculate_moneyline(spread),
            'overUnder': f"{(home_points + away_points):.1f}",
            'confidence': f"{min(max(abs(spread) * 10, 50), 95)}%",  # Scale confidence with spread
            'predictions': {
                'touchdowns': {
                    'home': home_touchdowns,
                    'away': away_touchdowns
                },
                'totalPoints': {
                    'home': home_points,
                    'away': away_points
                },
                'stats': {
                    'home': home_stats,
                    'away': away_stats
                }
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500

def calculate_moneyline(spread):
    # Convert spread to moneyline odds
    if spread < 0:
        return f"{int(-100 * (abs(spread)/3))}"
    else:
        return f"+{int(100 * (spread/3))}"

if name == 'main':
    app.run(host='0.0.0.0', port=10000)

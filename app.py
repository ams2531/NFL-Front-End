from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load the trained model at startup
model = joblib.load('nfl_model.joblib')

# Expanded teams dictionary with divisions
teams = {
    "AFC East": {
        "Buffalo Bills": ["Josh Allen", "Stefon Diggs"],
        "Miami Dolphins": ["Tua Tagovailoa", "Tyreek Hill"],
        "New England Patriots": ["Mac Jones", "Rhamondre Stevenson"],
        "New York Jets": ["Aaron Rodgers", "Garrett Wilson"]
    },
    "AFC North": {
        "Baltimore Ravens": ["Lamar Jackson", "Mark Andrews"],
        "Cincinnati Bengals": ["Joe Burrow", "Ja'Marr Chase"],
        "Cleveland Browns": ["Deshaun Watson", "Amari Cooper"],
        "Pittsburgh Steelers": ["Kenny Pickett", "Najee Harris"]
    },
    "AFC South": {
        "Houston Texans": ["C.J. Stroud", "Tank Dell"],
        "Indianapolis Colts": ["Anthony Richardson", "Jonathan Taylor"],
        "Jacksonville Jaguars": ["Trevor Lawrence", "Travis Etienne"],
        "Tennessee Titans": ["Will Levis", "DeAndre Hopkins"]
    },
    "AFC West": {
        "Denver Broncos": ["Russell Wilson", "Courtland Sutton"],
        "Kansas City Chiefs": ["Patrick Mahomes", "Travis Kelce"],
        "Las Vegas Raiders": ["Jimmy Garoppolo", "Davante Adams"],
        "Los Angeles Chargers": ["Justin Herbert", "Keenan Allen"]
    },
    "NFC East": {
        "Dallas Cowboys": ["Dak Prescott", "CeeDee Lamb"],
        "New York Giants": ["Daniel Jones", "Saquon Barkley"],
        "Philadelphia Eagles": ["Jalen Hurts", "A.J. Brown"],
        "Washington Commanders": ["Sam Howell", "Terry McLaurin"]
    },
    "NFC North": {
        "Chicago Bears": ["Justin Fields", "DJ Moore"],
        "Detroit Lions": ["Jared Goff", "Amon-Ra St. Brown"],
        "Green Bay Packers": ["Jordan Love", "Christian Watson"],
        "Minnesota Vikings": ["Kirk Cousins", "Justin Jefferson"]
    },
    "NFC South": {
        "Atlanta Falcons": ["Desmond Ridder", "Drake London"],
        "Carolina Panthers": ["Bryce Young", "Adam Thielen"],
        "New Orleans Saints": ["Derek Carr", "Chris Olave"],
        "Tampa Bay Buccaneers": ["Baker Mayfield", "Mike Evans"]
    },
    "NFC West": {
        "Arizona Cardinals": ["Kyler Murray", "Marquise Brown"],
        "Los Angeles Rams": ["Matthew Stafford", "Cooper Kupp"],
        "San Francisco 49ers": ["Brock Purdy", "Christian McCaffrey"],
        "Seattle Seahawks": ["Geno Smith", "DK Metcalf"]
    }
}

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        return jsonify({
            'success': True,
            'teams': teams
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        home_team = data.get('home_team')
        away_team = data.get('away_team')
        
        # Example: Extract features from input data (this needs to match your model's input format)
        features = [home_team, away_team]  # Replace with actual feature extraction logic
        features = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)
        
        return jsonify({
            'success': True,
            'prediction': prediction.tolist(),
            'home_team': home_team,
            'away_team': away_team,
            'message': 'Prediction made successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

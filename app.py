from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)  # Fix: Add underscores
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        home_team = data.get('homeTeam', '')
        away_team = data.get('awayTeam', '')
        
        # Your prediction logic here
        response = {
            'spread': f"{home_team} -3.5",
            'moneyline': "-150",
            'overUnder': "47.5",
            'confidence': "75%",
            'predictions': {
                'touchdowns': {
                    'home': 3.5,
                    'away': 2.8
                },
                'totalPoints': {
                    'home': 24,
                    'away': 21
                }
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':  # Fix: Add underscores
    app.run(host='0.0.0.0', port=10000)

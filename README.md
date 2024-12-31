# NFL Prediction API

This API provides NFL game predictions using a machine learning model.

## Features
- Predicts touchdowns for both teams
- Calculates spread and moneyline
- Uses team statistics for predictions

## Required Input Features
- YardsPerPlay (float)
- RushAttempts (int)
- PassAttempts (int)
- FirstDowns (int)

## Setup
1. Install requirements: pip install -r requirements.txt
2. Ensure model files are present:
   - nfl_model.joblib
   - nfl_scaler.joblib
3. Run the app: python app.py

## API Endpoints
POST /predict
```json
{
  "homeTeam": "Team Name",
  "awayTeam": "Team Name"
}
```

## Deploy
This app is designed to be deployed on Render.com

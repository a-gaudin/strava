# Strava logs insight
Visualize trainings logs from a [Strava](https://www.strava.com/) account and analyse factors causing short and long-term soreness and injuries.

* Language: Python
* Libraries: Pandas, Maplotlib, Scikit-learn

## Setup
1. [Activate the Strava API](https://developers.strava.com/docs/getting-started/) for your account with ```read-all``` access
2. Add a ```config.py``` file to fill in API request parameters, such as
```
token_request_params = {
    'client_id': "CLIENT_ID_TBD",
    'client_secret': 'CLIENT_SECRET_TBD',
    'refresh_token': 'REFRESH_TOKEN_TBD',
    'grant_type': "refresh_token",
    'f': 'json'
}

request_batch_size = 200 # limit is 200
```
3. Run ```create_activity_db.py``` (extracts all your Strava activities)
4. Run ```create_load_db.py``` (adds training load and injury notes)

## How to visualize your training data
1. Run ```create_summary_db.py``` (condenses data in a pivot table)
2. Run ```plot_summary.py``` (saves plots of activity history)
3. Open the file in the ```plot``` folder

## How to analyse factors causing injuries
1. Run ```create_injury_db.py``` (adds computed injury data)
2. Run ```create_injury_summary_db.py``` (condenses injury data in a pivot table)
3. Run ```plot_injury_factors.py``` (saves plots to analyze injury data)
4. Open the files in the ```plot``` folder

## Conclusions from my own Strava data
- To avoid fatigue injuries: Prefer rides to runs and decrease training time
- To avoid injuries/soreness on the spot: prefer low-intensity sessions, and climbs to longer sessions (Major factors: 1. Perceived exertion, 2. Distance, 3. Elevation gain, 4. Grade asjued speed)
- Training load does not have a major impact on injuries, a relevant training plan can combine heavy loads and the absence of injuries

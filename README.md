# Strava logs insights
Visualize trainings logs from a Strava account (https://www.strava.com/)

* Language: Python
* Libraries: Pandas, Scikit-learn

## Instructions:
1. Activate the Strava API with ```read-all``` access
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
2. Run ```init_activities_db.py``` to extract all your Strava activities into a pickle database
3. Run ```init_activities_load.py``` to add soreness and injury to the pickle database
4. Run ```view.py``` to visualize 
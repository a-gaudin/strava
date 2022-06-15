import config
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI:
    def __init__(self) -> None:
        self.__activities_url = 'https://www.strava.com/api/v3/activities/'
        self.header = self.__get_header()
    
    def __get_header(self) -> dict:
        """ Get request header for Strava request
        Returns:
            (dict): request header
        """
        auth_url = 'https://www.strava.com/oauth/token'
        res = requests.post(auth_url, data=config.token_request_params, verify=False)
        access_token = res.json()['access_token']
        return {'Authorization': f'Bearer {access_token}'}

    def get_activity(self, id:int) -> str:
        """ Get one Strava activity's data
        Args:
            id (int): Strava activity id
        Returns:
            (str): JSON of the activity data
        """
        activity_url = self.__activities_url + str(id)
        params = {
            'include_all_efforts': False
        }
        return requests.get(activity_url, headers=self.header, params=params).json()

    def get_all_activities(self) -> str:
        """ Get all Strava activities data
        Returns:
            (str): JSON of all activities data
        """
        run_new_request = True
        page = 1
        activities_json = []

        while run_new_request == True:
            params = {
                'per_page': config.request_batch_size,
                'page': page
            }
            new_activities_json = requests.get(self.__activities_url, headers=self.header, params=params).json()
            print(f'Strava API response message: {new_activities_json}')
            activities_json += new_activities_json
            page += 1

            if len(new_activities_json) < config.request_batch_size:
                run_new_request = False

        return activities_json

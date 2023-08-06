import requests
import datetime
from pandas import json_normalize




def get_games(api_key, cursor):
    odds = json_normalize(requests.get("https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/",
                        params={'apiKey': api_key,
                                'regions': 'us',
                                'markets': 'h2h'}).json())


    for i in odds.index:
        game_id = odds['id'][i]
        home_team = odds['home_team'][i]
        away_team = odds['away_team'][i]
        start_time = odds['commence_time'][i]
        time_added = datetime.datetime.now()

        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM hockey_games WHERE game_id = '{game_id}')")

        if cursor.fetchone()[0]==True:
            pass
        else:
            cursor.execute("INSERT INTO hockey_games VALUES(%s, %s, %s, %s, %s)", (game_id, home_team, away_team, start_time, time_added))


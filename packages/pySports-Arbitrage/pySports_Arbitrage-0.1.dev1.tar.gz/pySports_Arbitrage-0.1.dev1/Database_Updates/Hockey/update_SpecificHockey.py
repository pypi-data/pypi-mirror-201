import requests
import datetime
from pandas import json_normalize

def getSpecific_odds(gameid, api_key, cursor):
    odds = json_normalize(requests.get("https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/",
                        params={'apiKey': api_key,
                                'regions': 'us',
                                'markets': 'h2h'}).json())


    for index, row in odds.iterrows():
        if odds['id'][index] == gameid:

            home_team = row['home_team']
            away_team = row['away_team']
            for x in row['bookmakers']:
                bookie = x['title']
                time_updated = x['last_update']
                time_requested = datetime.datetime.now()
                for odd in x['markets'][0]['outcomes']:
                    if odd['name'] == home_team:
                        home_odds = odd['price']
                    elif odd['name'] == away_team:
                        away_odds = odd['price']
                cursor.execute("INSERT INTO hockey_odds VALUES (%s, %s, %s, %s, %s, %s)", (gameid, bookie, home_odds,
                                away_odds, time_updated, time_requested))

        else:
            pass

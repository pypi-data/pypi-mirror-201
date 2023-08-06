import datetime
import requests
from pandas import json_normalize




def getHockeyOdds(api_key, cursor):
    odds = json_normalize(requests.get("https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/",
                        params={'apiKey': api_key,
                                'regions': 'us',
                                'markets': 'h2h'}).json())

    # conn = psycopg2.connect(database=database, host=db_host,user=db_user,password=db_pass, port=db_port)
    # conn.autocommit = True
    #
    # cursor = conn.cursor()


    for i in odds.index:
        game_id = odds['id'][i]
        home_team = odds['home_team'][i]
        away_team = odds['away_team'][i]

        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM hockey_games WHERE game_id = '{game_id}')")

        if cursor.fetchone()[0]==True:
            for x in odds['bookmakers'][i]:
                bookie = x['title']
                time_updated = x['last_update']             #time upd is from api
                time_requested = datetime.datetime.now()    # time req is actual time of req
                for odd in x['markets'][0]['outcomes']:
                    if odd['name'] == home_team:
                        home_odds = odd['price']
                    elif odd['name'] == away_team:
                        away_odds = odd['price']
                cursor.execute("INSERT INTO hockey_odds VALUES (%s, %s, %s, %s, %s, %s)", (game_id, bookie, home_odds,
                               away_odds, time_updated, time_requested))
        else:
            pass

from datetime import datetime, timedelta

import jmespath
import requests


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# print(Color.BOLD + 'Hello World !' + Color.END)

yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

goalies = requests.get("https://api.nhle.com/stats/rest/ru/goalie/summary?isAggregate=false&isGame=false&sort=%5B%7B"
                       "%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22savePct%22,"
                       "%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp"
                       "=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
goalies_parsed = jmespath.search("data[].{goalie: goalieFullName, team: teamAbbrevs saves: savePct, wins: wins}",
                                 goalies)

print(goalies_parsed)
n = 1
for index, item in zip(range(10), goalies_parsed):
    print(
        str(n) + ". " + item['goalie'] + " " + item['team'] + " C:" + str(round(item['saves'] * 100, 2)) + "% П:" + str(
            item['wins']))
    n = n + 1

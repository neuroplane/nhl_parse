import jmespath
import requests

field_players = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22"
    ":%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,"
    "%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E"
    "=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()

field_players_parsed = jmespath.search(
    "data[].{name: skaterFullName, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, "
    "points: points, plusminus: plusMinus}",
    field_players)

print(field_players_parsed)
n = 1
for index, item in zip(range(10), field_players_parsed):
    print(str(n) + ". " + item['name'] + ", " + item['team'] + ", " + item['position'] + ", " + str(
        item['goals']) + "-" + str(item['assists']) + "-" + str(item['points']) + ", ±" + str(item['plusminus']))
    n = n + 1

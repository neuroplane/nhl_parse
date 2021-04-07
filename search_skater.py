import json
import os
import sys

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timezone, timedelta
##########################################################
now = datetime.today().strftime('%H:%M:%S')
now_file = datetime.today().strftime('%H%M%S')
now_date = datetime.today().strftime('%d.%m.%Y')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
#SCORES#########################################################
#last_games = requests.get(
#    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=ru_nhl&teamId=&gameType=&timecode=").json()
#last_games_parsed = jmespath.search(
#    "dates[].games[].{otstatus: linescore. currentPeriod, away: {team: teams.away.team.teamName, loc: teams.away.team.locationName, score: teams.away.score},home:{team: teams.home.team.teamName, loc: teams.home.team.locationName, score: teams.home.score}}",
#    last_games)
first_skater = input('First skater search\t')
second_skater = input('Second player search:\t')
#STATS#########################################################
first_skater_json = requests.get(
    "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=true&isGame=false&sort=%5B%7B%22property%22:%22timeOnIcePerGame%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=19781979%20and%20skaterFullName%20likeIgnoreCase%20%22%25"+first_skater+"%25%22").json()
first_skater_json_parsed = jmespath.search(
    "data[].{name: skaterFullName, ppg: ppGoals, gp: gamesPlayed, toi: timeOnIcePerGame, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    first_skater_json)
second_skater_json = requests.get(
    "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=true&isGame=false&sort=%5B%7B%22property%22:%22timeOnIcePerGame%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=19781979%20and%20skaterFullName%20likeIgnoreCase%20%22%25"+second_skater+"%25%22").json()
second_skater_json_parsed = jmespath.search(
    "data[].{name: skaterFullName, ppg: ppGoals, gp: gamesPlayed, toi: timeOnIcePerGame, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    second_skater_json)

for first in first_skater_json_parsed:
    print(first['name'] + ": " + str(round(first['toi'] * first['gp'] / first['goals'] / 60, 1)))
for second in second_skater_json_parsed:
    print(second['name'] + ": " + str(round(second['toi'] * second['gp'] / second['goals'] / 60, 1)))

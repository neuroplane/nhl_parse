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
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
#SCORES#########################################################
last_games = requests.get(
    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=ru_nhl&teamId=&gameType=&timecode=").json()
last_games_parsed = jmespath.search(
    "dates[].games[].{otstatus: linescore. currentPeriod, away: {team: teams.away.team.teamName, loc: teams.away.team.locationName, score: teams.away.score},home:{team: teams.home.team.teamName, loc: teams.home.team.locationName, score: teams.home.score}}",
    last_games)
#STATS#########################################################
field_players = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_parsed = jmespath.search(
    "data[].{name: skaterFullName, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    field_players)
#STATS#########################################################
field_players_rus = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20nationalityCode=%22RUS%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_rus_parsed = jmespath.search(
    "data[].{name: lastName, team: teamAbbrevs, goals: goals, assists: assists, points: points, plusminus: plusMinus, gwg: gameWinningGoals, position: positionCode ,shots: shots,pointspg: pointsPerGame}",
    field_players_rus)
print(field_players_parsed)
#STATS_RUS#####################################################
#GOALIES#######################################################
#SCORES########################################################
#SCORES########################################################
#with Image.open("pics/stats.png") as im:
with Image.open("pics/stanley.png") as im:
    SCW = 1668
    SCH = 2388
    LINE_HEIGHT = 63
    LINE_H = 60
    START_Y_SCORES = 100
    GREY = (220, 220, 220, 128)
    SHADOW = (50, 50, 50)
    boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
    robotocond = ImageFont.truetype('fonts/robotocond.ttf', 48)
    mach = ImageFont.truetype('fonts/mach.otf', 40)
    machsmall = ImageFont.truetype('fonts/mach.otf', 25)
    machbig = ImageFont.truetype('fonts/mach.otf', 120)
    unreal = ImageFont.truetype('fonts/unreal.ttf', 50)
    ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 55)
    ubuntuс = ImageFont.truetype('fonts/ubuntuc.ttf', 65)
    def_font = ubuntu
    draw = ImageDraw.Draw(im)
    #draw.rectangle([(0, 40), (SCW, 120)], fill=(0, 0, 0, 228), outline=None)
    #draw.text((SCW/2, 80), 'РЕЗУЛЬТАТЫ НА ' + str(yesterday_rus), font=machbig, fill='white', anchor='mm')
    ###### FIELD PLAYERS DRAW
    START_Y_FIELDPLAYERS = START_Y_SCORES + LINE_HEIGHT
    draw.line((50,  START_Y_FIELDPLAYERS+LINE_HEIGHT, SCW - 50, START_Y_FIELDPLAYERS+LINE_HEIGHT), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS-30), 'БОМБАРДИРЫ ЛИГИ', font=machbig, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.line((50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2, SCW - 50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2), fill=GREY,
              width=1)
    pos_num = 100
    pos_position = pos_num + 80
    pos_name = pos_position + 100
    pos_team = pos_name + 700
    pos_goals = pos_team + 350  # 180
    #pos_assists = pos_goals + 190  # 210
    pos_points = pos_goals + 200  # 240
    pos_plusminus = pos_points + 250  # 270
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.text((pos_num, START_Y_FIELDPLAYERS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS), "Г", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_assists, START_Y_FIELDPLAYERS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_points, START_Y_FIELDPLAYERS), "О", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_plusminus, START_Y_FIELDPLAYERS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + 120
    for index, item in zip(range(10), field_players_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS), item['position'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_goals, START_Y_FIELDPLAYERS), str(item['goals']), font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_assists, START_Y_FIELDPLAYERS), str(item['assists']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_points, START_Y_FIELDPLAYERS), str(item['points']), font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_plusminus, START_Y_FIELDPLAYERS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT

    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS + LINE_HEIGHT*3
    draw.line((50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS, SCW - 50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS_RUS-30), 'БОМБАРДИРЫ ЛИГИ ИЗ РОССИИ', font=machbig, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    draw.line((50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT, SCW - 50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT), fill=GREY,
              width=1)
    draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS_RUS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS_RUS), "Г", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), "Пас", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), "О", font=def_font, fill=GREY, anchor="lm")
    #draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    for index, item in zip(range(10), field_players_rus_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS_RUS), item['position'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_goals, START_Y_FIELDPLAYERS_RUS), str(item['goals']), font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), str(item['assists']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), str(item['points']), font=def_font, fill=GREY, anchor="lm")
        #draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT

    # write to stdout
    print(json.dumps(field_players_rus_parsed, ensure_ascii=False, indent=2))
    im.show()

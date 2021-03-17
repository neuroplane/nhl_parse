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
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_parsed = jmespath.search(
    "data[].{name: skaterFullName, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    field_players)

print(field_players_parsed)
#STATS_RUS#####################################################
#GOALIES#######################################################
#SCORES########################################################
#SCORES########################################################
with Image.open("pics/stats.png") as im:
    SCW = 800
    SCH = 800
    LINE_HEIGHT = 65
    START_Y_SCORES = 200
    GREY = (220, 220, 220, 128)
    SHADOW = (50, 50, 50)
    boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
    robotocond = ImageFont.truetype('fonts/robotocond.ttf', 48)
    mach = ImageFont.truetype('fonts/mach.otf', 40)
    machsmall = ImageFont.truetype('fonts/mach.otf', 25)
    machbig = ImageFont.truetype('fonts/mach.otf', 60)
    unreal = ImageFont.truetype('fonts/unreal.ttf', 50)
    ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 50)
    def_font = ubuntu
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 40), (800, 120)], fill=(0, 0, 0, 228), outline=None)
    draw.text((400, 80), 'РЕЗУЛЬТАТЫ ЗА ' + str(yesterday_rus), font=machbig, fill='white', anchor='mm')
    ###### FIELD PLAYERS DRAW
    START_Y_FIELDPLAYERS = START_Y_SCORES + 30
    draw.text((SCW / 2, START_Y_FIELDPLAYERS), ' ^q ^~ ^| ^q ^p   ^t ^x    ', font=def_font, fill=0, anchor="mm")
    draw.line((10, LINE_HEIGHT + START_Y_FIELDPLAYERS, SCW - 10, LINE_HEIGHT + START_Y_FIELDPLAYERS), fill=0, width=1)
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT * 2
    pos_num = 100
    pos_name = pos_num + 35
    pos_team = pos_name + 520  # 130
    pos_position = pos_team + 190  # 155
    pos_goals = pos_position + 190  # 180
    pos_assists = pos_goals + 190  # 210
    pos_points = pos_assists + 190  # 240
    pos_plusminus = pos_points + 190  # 270

    draw.text((pos_num, START_Y_FIELDPLAYERS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS), "Поз", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS), "Гол", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_assists, START_Y_FIELDPLAYERS), "Пас", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_points, START_Y_FIELDPLAYERS), "ОЧК", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_plusminus, START_Y_FIELDPLAYERS), "+/-", font=def_font, fill=GREY, anchor="rm")
    draw.line((10, START_Y_FIELDPLAYERS + LINE_HEIGHT, SCW - 10, START_Y_FIELDPLAYERS + LINE_HEIGHT), fill=0, width=1)
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT * 2
    for index, item in zip(range(10), field_players_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS), item['position'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_goals, START_Y_FIELDPLAYERS), str(item['goals']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_assists, START_Y_FIELDPLAYERS), str(item['assists']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_points, START_Y_FIELDPLAYERS), str(item['points']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_plusminus, START_Y_FIELDPLAYERS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT

    START_Y_SCORES = START_Y_SCORES + LINE_HEIGHT
    # write to stdout
    print(last_games_parsed)
    im.show()

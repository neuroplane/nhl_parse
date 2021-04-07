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
#STATS#########################################################
field_players = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_parsed = jmespath.search(
    "data[].{name: skaterFullName, ppg: ppGoals, gp: gamesPlayed, toi: timeOnIcePerGame, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    field_players)
#STATS#########################################################
field_players_rus = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20nationalityCode=%22RUS%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_rus_parsed = jmespath.search(
    "data[].{name: lastName, team: teamAbbrevs, gp: gamesPlayed, toi: timeOnIcePerGame, goals: goals, assists: assists, points: points, plusminus: plusMinus, gwg: gameWinningGoals, position: positionCode ,shots: shots,pointspg: pointsPerGame}",
    field_players_rus)
print(field_players_parsed)
#STATS_RUS#####################################################
#GOALIES#######################################################
#SCORES########################################################
#SCORES########################################################
#with Image.open("pics/stats.png") as im:
with Image.open("pics/highlights.jpg") as im:
    SCW, SCH = im.size
    print(im.size)
    #SCW = 1668
    #SCH = 2388
    LINE_HEIGHT = 85
    LINE_H = 60
    START_Y_SCORES = 100
    GREY = (230, 230, 230, 128)
    SHADOW = (50, 50, 50)
    boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
    robotocond = ImageFont.truetype('fonts/robotocond.ttf', 48)
    mach = ImageFont.truetype('fonts/mach.otf', 40)
    machsmall = ImageFont.truetype('fonts/mach.otf', 25)
    machbig = ImageFont.truetype('fonts/mach.otf', 140)
    unreal = ImageFont.truetype('fonts/unreal.ttf', 50)
    ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 65)
    ubuntuс = ImageFont.truetype('fonts/ubuntuc.ttf', 65)
    kroftsman = ImageFont.truetype('fonts/kroftsman.ttf', 150)
    kroftsmansm = ImageFont.truetype('fonts/kroftsman.ttf', 150)
    def_font = ubuntu
    draw = ImageDraw.Draw(im)
    #draw.rectangle([(0, 40), (SCW, 120)], fill=(0, 0, 0, 228), outline=None)
    #draw.text((SCW/2, 80), 'РЕЗУЛЬТАТЫ НА ' + str(yesterday_rus), font=machbig, fill='white', anchor='mm')
    ###### FIELD PLAYERS DRAW
    START_Y_FIELDPLAYERS = START_Y_SCORES + LINE_HEIGHT
    draw.line((50,  START_Y_FIELDPLAYERS+LINE_HEIGHT, SCW - 50, START_Y_FIELDPLAYERS+LINE_HEIGHT), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS-30), 'СНАЙПЕРЬ', font=kroftsman, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.line((50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2, SCW - 50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2), fill=GREY,
              width=1)
    pos_num = round(SCW*0.07)
    pos_position = round(SCW * 0.12)
    pos_name = round(SCW * 0.19)
    pos_team = round(SCW * 0.55)
    pos_goals = round(SCW * 0.71)  # 180
    #pos_assists = pos_goals + 190  # 210
    pos_points = round(SCW * 0.81)  # 240
    pos_plusminus = pos_points + 250  # 270
    pos_mog = round(SCW * 0.96)
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.text((pos_num, START_Y_FIELDPLAYERS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS), "Г", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_assists, START_Y_FIELDPLAYERS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_points, START_Y_FIELDPLAYERS), "О", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_mog, START_Y_FIELDPLAYERS), "мин/г", font=def_font, fill=GREY, anchor="rm")

    #draw.text((pos_plusminus, START_Y_FIELDPLAYERS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
    for index, item in zip(range(10), field_players_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS), item['position'], font=def_font, fill=GREY, anchor="lm")
        #draw.rectangle(((pos_goals - 130, START_Y_FIELDPLAYERS-LINE_HEIGHT/2), (pos_goals + 30, START_Y_FIELDPLAYERS + LINE_HEIGHT)), fill="#4c4cd9")
        draw.text((pos_goals, START_Y_FIELDPLAYERS), str(item['goals']), font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_assists, START_Y_FIELDPLAYERS), str(item['assists']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_points, START_Y_FIELDPLAYERS), str(item['points']), font=def_font, fill=GREY, anchor="rm")
        toi = str(round(item['toi'] * item['gp'] / item['goals'] / 60))
        draw.text((pos_mog, START_Y_FIELDPLAYERS), toi, font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_plusminus, START_Y_FIELDPLAYERS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
        print(item['name'] + ", MOG: " + toi + ', ' + str(item['goals']) + ', ' + str(item['toi']) + ', ' + str(item['gp']) + ', ' + str(round(item['assists']/item['goals'], 2)))

    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
    draw.line((50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS, SCW - 50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS_RUS-30), 'СНАЙПЕРЬ ИЗ РОССИИ', font=kroftsman, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    draw.line((50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT, SCW - 50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT), fill=GREY,
              width=1)
    draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_position, START_Y_FIELDPLAYERS_RUS), "П", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_goals, START_Y_FIELDPLAYERS_RUS), "Г", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), "Пас", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), "О", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_mog, START_Y_FIELDPLAYERS_RUS), "мин/г", font=def_font, fill=GREY, anchor="rm")
    #draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    for index, item in zip(range(10), field_players_rus_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_position, START_Y_FIELDPLAYERS_RUS), item['position'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_goals, START_Y_FIELDPLAYERS_RUS), str(item['goals']), font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), str(item['assists']), font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), str(item['points']), font=def_font, fill=GREY, anchor="rm")
        toi = str(round(item['toi'] * item['gp'] / item['goals'] / 60))
        draw.text((pos_mog, START_Y_FIELDPLAYERS_RUS), toi, font=def_font, fill=GREY, anchor="rm")
        #draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT
    draw.text((70, SCH-60), str(now_date), font=kroftsmansm, fill=GREY, anchor="lb")
    # write to stdout
    #print(json.dumps(field_players_rus_parsed, ensure_ascii=False, indent=2))
    size = (167*4, 239*4)
    out = im.resize(size)
    out.show()
    #out.save('pics/out' + now_file + '.png')
    #print(last_games)

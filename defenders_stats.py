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
#STATS#########################################################
field_players = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=3%20and%20positionCode%3D%22D%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_parsed = jmespath.search(
    "data[].{playerId: playerId, name: skaterFullName, ppg: ppGoals, gp: gamesPlayed, toi: timeOnIcePerGame, team: teamAbbrevs, position: positionCode, goals: goals, assists: assists, points: points, plusminus: plusMinus}",
    field_players)
#STATS#########################################################
field_players_rus = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1%20and%20gamesPlayed%3E=1&cayenneExp=gameTypeId=3%20and%20nationalityCode=%22RUS%22%20and%20positionCode%3D%22D%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
field_players_rus_parsed = jmespath.search(
    "data[].{playerId: playerId, name: skaterFullName, team: teamAbbrevs, goals: goals, assists: assists, points: points, plusminus: plusMinus, gwg: gameWinningGoals, position: positionCode ,shots: shots,pointspg: pointsPerGame}",
    field_players_rus)
defs = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/realtime?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22missedShots%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=3%20and%20positionCode%3D%22D%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021"
).json()
defs_parsed = jmespath.search("data[].{takeaways: takeaways, blockedShots: blockedShots, pid: playerId, name: skaterFullName, hits:hits, bs: blockedShots}", defs
)
defs_rus = requests.get(
    "https://api.nhle.com/stats/rest/ru/skater/realtime?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22missedShots%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=3%20and%20positionCode%3D%22D%22%20and%20nationalityCode=%22RUS%22%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021"
).json()
defs_rus_parsed = jmespath.search("data[].{takeaways: takeaways, blockedShots: blockedShots, pid: playerId, name: skaterFullName, hits:hits, bs: blockedShots}", defs_rus
)
print(defs_rus)

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
    ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 60)
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
    draw.text((SCW / 2, START_Y_FIELDPLAYERS-30), 'ЗАЩИТНИКИ', font=kroftsman, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.line((50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2, SCW - 50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2), fill=GREY,
              width=1)
    ### COORDINATES
    pos_num = round(SCW*0.06)
    pos_position = round(SCW * 0.9)
    pos_name = round(SCW * 0.10)
    pos_team = round(SCW * 0.43)
    ##############
    pos_points = round(SCW * 0.57)  #
    pos_assists = round(SCW * 0.65)  # 210
    pos_blocks = round(SCW * 0.73)  # BLOCKS
    pos_hits = round(SCW * 0.81)
    pos_takeaways = round(SCW * 0.89)
    pos_plusminus = round(SCW * 0.97)  # 270
    ##############
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.text((pos_num, START_Y_FIELDPLAYERS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_blocks, START_Y_FIELDPLAYERS), "Блк", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_assists, START_Y_FIELDPLAYERS), "Пас", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_points, START_Y_FIELDPLAYERS), "Очк", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_hits, START_Y_FIELDPLAYERS), "Хит", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_takeaways, START_Y_FIELDPLAYERS), "Отб", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_plusminus, START_Y_FIELDPLAYERS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
    for index, item in zip(range(10), field_players_parsed):
        draw.text((pos_num, START_Y_FIELDPLAYERS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_assists, START_Y_FIELDPLAYERS), str(item['assists']), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_points, START_Y_FIELDPLAYERS), str(item['points']), font=def_font, fill=GREY, anchor="rm")
        for def_hits in defs_parsed:
            if def_hits['pid'] == item['playerId']:
                draw.text((pos_hits, START_Y_FIELDPLAYERS), str(def_hits['hits']), font=def_font, fill=GREY,
                          anchor="rm")
                draw.text((pos_blocks, START_Y_FIELDPLAYERS), str(def_hits['blockedShots']), font=def_font, fill=GREY, anchor="rm")
                draw.text((pos_takeaways, START_Y_FIELDPLAYERS), str(def_hits['takeaways']), font=def_font, fill=GREY,
                          anchor="rm")
        draw.text((pos_plusminus, START_Y_FIELDPLAYERS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT

    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
    draw.line((50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS, SCW - 50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS_RUS-30), 'ЗАЩИТНИКИ ИЗ РОССИИ', font=kroftsman, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    draw.line((50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT, SCW - 50, START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT), fill=GREY,
              width=1)
    draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), '#', font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), "Имя", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), "Ком", font=def_font, fill=GREY, anchor="lm")
    draw.text((pos_blocks, START_Y_FIELDPLAYERS_RUS), "Блк", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), "Пас", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), "Очк", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_hits, START_Y_FIELDPLAYERS_RUS), "Хит", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_takeaways, START_Y_FIELDPLAYERS_RUS), "Отб", font=def_font, fill=GREY, anchor="rm")
    draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), "+/-", font=def_font, fill=GREY, anchor="rm")
    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT * 2
    for index, item in zip(range(10), field_players_rus_parsed):
        if (item['name'] == 'Artem Zub'):
            item['name'] = 'Артём Зуб'
        elif (item['name'] == 'Nikolai Knyzhov'):
            item['name'] = 'Николай Кныжов'
        elif (item['name'] == 'Alexander Romanov'):
            item['name'] = 'Александр Романов'
        draw.text((pos_num, START_Y_FIELDPLAYERS_RUS), str(index + 1), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_name, START_Y_FIELDPLAYERS_RUS), item['name'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_team, START_Y_FIELDPLAYERS_RUS), item['team'], font=def_font, fill=GREY, anchor="lm")
        draw.text((pos_assists, START_Y_FIELDPLAYERS_RUS), str(item['assists']), font=def_font, fill=GREY, anchor="rm")
        draw.text((pos_points, START_Y_FIELDPLAYERS_RUS), str(item['points']), font=def_font, fill=GREY, anchor="rm")
        for def_hits in defs_rus_parsed:
            if def_hits['pid'] == item['playerId']:
                draw.text((pos_hits, START_Y_FIELDPLAYERS_RUS), str(def_hits['hits']), font=def_font, fill=GREY,
                          anchor="rm")
                draw.text((pos_blocks, START_Y_FIELDPLAYERS_RUS), str(def_hits['blockedShots']), font=def_font, fill=GREY,
                          anchor="rm")
                draw.text((pos_takeaways, START_Y_FIELDPLAYERS_RUS), str(def_hits['takeaways']), font=def_font, fill=GREY,
                          anchor="rm")
        draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT
    draw.text((70, SCH-60), str(now_date), font=kroftsmansm, fill=GREY, anchor="lb")
    size = (167*4, 239*4)
    out = im.resize(size)
    out.show()
    out.save('rendered/out' + now_file + '_defenders.png')

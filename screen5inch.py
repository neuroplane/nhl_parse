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
    draw.text((SCW / 2, START_Y_FIELDPLAYERS-30), 'БОМБАРДИРЬ ПЛЕЙ-ОФФ', font=kroftsman, fill=GREY, anchor="mm")
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT
    draw.line((50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2, SCW - 50, START_Y_FIELDPLAYERS + LINE_HEIGHT*2), fill=GREY,
              width=1)
    pos_num = round(SCW*0.07)
    pos_position = round(SCW * 0.12)
    pos_name = round(SCW * 0.19)
    pos_team = round(SCW * 0.65)
    pos_goals = round(SCW * 0.84)  # 180
    #pos_assists = pos_goals + 190  # 210
    pos_points = round(SCW * 0.96)  # 240
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
    START_Y_FIELDPLAYERS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
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
        #toi = str(round(item['toi']*item['gp']/item['goals']/60, 2))
        #print(item['name'] + ", минут/гол: " + toi + ", индекс читера: " + str(round(item['ppg']/item['goals'], 2)))

    START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS + LINE_HEIGHT*2
    draw.line((50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS, SCW - 50, LINE_HEIGHT + START_Y_FIELDPLAYERS_RUS), fill=GREY, width=1)
    draw.text((SCW / 2, START_Y_FIELDPLAYERS_RUS-30), 'БОМБАРДИРЬ ИЗ РОССИИ', font=kroftsman, fill=GREY, anchor="mm")
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
        #draw.text((pos_plusminus, START_Y_FIELDPLAYERS_RUS), str(item['plusminus']), font=def_font, fill=GREY, anchor="rm")
        START_Y_FIELDPLAYERS_RUS = START_Y_FIELDPLAYERS_RUS + LINE_HEIGHT
    draw.text((70, SCH-60), str(now_date), font=kroftsmansm, fill=GREY, anchor="lb")
    # write to stdout
    #print(json.dumps(field_players_rus_parsed, ensure_ascii=False, indent=2))
    size = (167*4, 239*4)
    out = im.resize(size)
    out.show()
    out.save('rendered/out' + now_file + '_bombardiers.png')

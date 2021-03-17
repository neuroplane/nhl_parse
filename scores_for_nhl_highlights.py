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
##########################################################
last_games = requests.get(
    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=ru_nhl&teamId=&gameType=&timecode=").json()
last_games_parsed = jmespath.search(
    "dates[].games[].{otstatus: linescore. currentPeriod, away: {team: teams.away.team.teamName, loc: teams.away.team.locationName, score: teams.away.score},home:{team: teams.home.team.teamName, loc: teams.home.team.locationName, score: teams.home.score}}",
    last_games)

with Image.open("pics/800.png") as im:
    SCW = 800
    SCH = 800
    LINE_HEIGHT = 45
    START_Y_SCORES = 200
    GREY = (220, 220, 220, 128)
    SHADOW = (50, 50, 50)
    boston = ImageFont.truetype('fonts/nhlboston.ttf', 24)
    robotocond = ImageFont.truetype('fonts/robotocond.ttf', 28)
    mach = ImageFont.truetype('fonts/mach.otf', 40)
    machsmall = ImageFont.truetype('fonts/mach.otf', 25)
    machbig = ImageFont.truetype('fonts/mach.otf', 60)
    unreal = ImageFont.truetype('fonts/unreal.ttf', 60)
    def_font = mach
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 40), (800, 120)], fill=(0, 0, 0, 228), outline=None)
    draw.text((400, 80), 'РЕЗУЛЬТАТЫ ЗА ' + str(yesterday_rus), font=machbig, fill='white', anchor='mm')
    for item in last_games_parsed:
        line_away = str.strip(item['away']['loc'].upper()) #+ "  " + str.upper(item['away']['team'])
        line_score = str(item['away']['score']) + " : " + str(item['home']['score'])
        line_home = str.upper(item['home']['loc']) #+ "  " + str.upper(item['home']['team'])
        # print(w)
        # draw.rectangle((START_X,START_Y, 11, 11), fill = 0)
        ################################### SHADOW
        draw.text((SCW / 2 - 70 - 1 , START_Y_SCORES-1), line_away, font=def_font, fill=SHADOW, anchor="rm")
        draw.text((SCW / 2 - 1, START_Y_SCORES-1), line_score, font=def_font, fill=SHADOW, anchor="mm")
        draw.text((SCW / 2 + 70 - 1, START_Y_SCORES-1), line_home, font=def_font, fill=SHADOW, anchor="lm")
        ################################### TEXT
        draw.text((SCW / 2 - 70, START_Y_SCORES), line_away, font=def_font, fill=GREY, anchor="rm")
        draw.text((SCW / 2, START_Y_SCORES), line_score, font=def_font, fill=GREY, anchor="mm")
        if item['otstatus'] == 4:
            draw.text((SCW / 2 + 33, START_Y_SCORES - 1 + 5), 'OT', font=machsmall, fill=GREY, anchor="lb")
        elif item['otstatus'] == 5:
            draw.text((SCW / 2 + 33, START_Y_SCORES - 1 + 5), 'Б', font=machsmall, fill=GREY, anchor="lb")
        draw.text((SCW / 2 + 70, START_Y_SCORES), line_home, font=def_font, fill=GREY, anchor="lm")

        START_Y_SCORES = START_Y_SCORES + LINE_HEIGHT
    # write to stdout
    print(last_games_parsed)
    im.show()

import json
import os
import sys
from operator import itemgetter

import jmespath
import requests
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, timezone, timedelta


def get_teams_stats():
    now = datetime.today().strftime('%H:%M:%S')
    now_file = datetime.today().strftime('%H%M%S')
    now_date = datetime.today().strftime('%d.%m.%Y')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')

    stats_misc = requests.get("https://api.nhle.com/stats/rest/ru/team/realtime?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22hits%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
    stats_misc_parsed = jmespath.search("data[].{teamFullName: teamFullName, hits:hits, blockedShots: blockedShots, giveaways: giveaways, takeaways: takeaways, missedShots: missedShots}", stats_misc)
    stats_shots = requests.get("https://api.nhle.com/stats/rest/ru/team/shottype?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22shotsOnNetBackhand%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
    stats_shots_parsed = jmespath.search("data[].{teamFullName: teamFullName, shotsOnNet: shotsOnNet, shootingPct: shootingPct}", stats_shots)
    stats_penalties = requests.get("https://api.nhle.com/stats/rest/ru/team/penalties?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22penaltyMinutes%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=50&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20202021%20and%20seasonId%3E=20202021").json()
    stats_penalties_parsed = jmespath.search("data[].{teamFullName: teamFullName, penaltyMinutes: penaltyMinutes}", stats_penalties)

    sorting_type = False
    stats_misc_parsed_hits_reduced = sorted(stats_misc_parsed, key=itemgetter('hits'), reverse=sorting_type)[:5]
    stats_misc_parsed_blocks_reduced = sorted(stats_misc_parsed, key=itemgetter('blockedShots'), reverse=sorting_type)[:5]
    stats_misc_parsed_missed_reduced = sorted(stats_misc_parsed, key=itemgetter('missedShots'), reverse=sorting_type)[:5]
    stats_misc_parsed_giveaways_reduced = sorted(stats_misc_parsed, key=itemgetter('giveaways'), reverse=sorting_type)[:5]
    stats_misc_parsed_takeaways_reduced = sorted(stats_misc_parsed, key=itemgetter('takeaways'), reverse=sorting_type)[:5]
    stats_shots_parsed_shootingPct_reduced = sorted(stats_shots_parsed, key=itemgetter('shootingPct'), reverse=sorting_type)[:5]
    stats_shots_parsed_shotsOnNet_reduced = sorted(stats_shots_parsed, key=itemgetter('shotsOnNet'), reverse=sorting_type)[:5]
    stats_penalties_parsed_penaltyMinutes_reduced = sorted(stats_penalties_parsed, key=itemgetter('penaltyMinutes'), reverse=sorting_type)[:5]
    with Image.open("pics/highlights.jpg") as im:
        SCW, SCH = im.size
        print(im.size)
        print(SCW/4, SCH)
        LINE_HEIGHT = 70
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
        ubuntu = ImageFont.truetype('fonts/Ubuntu-M.ttf', 50)
        ubuntuc = ImageFont.truetype('fonts/ubuntuc.ttf', 55)
        kroftsman = ImageFont.truetype('fonts/kroftsman.ttf', 150)
        kroftsmansm = ImageFont.truetype('fonts/kroftsman.ttf', 100)
        def_font = ubuntu
        draw = ImageDraw.Draw(im)
        ###### FIELD PLAYERS DRAW
        margin_horizontal = 30
        pos_column_1_center = round(SCW * 0.25)
        pos_column_1_start = margin_horizontal
        pos_column_1_end = SCW/2 - margin_horizontal
        pos_column_2_center = round(SCW * 0.75)
        pos_column_2_start = SCW/2 + margin_horizontal
        pos_column_2_end = SCW - margin_horizontal
        row_1_start = 400
        row_2_start = row_1_start + 600
        row_3_start = row_2_start + 600
        row_4_start = row_3_start + 600
        draw_start = START_Y_SCORES + LINE_HEIGHT
        draw.text((SCW/2, row_1_start-280), 'НАИМЕНЫШИЕ ПОКАЗАТЕЛИ', font=kroftsman, fill=GREY, anchor="mm")
        draw.text((pos_column_1_center, row_1_start), 'ХИТЬ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_1_start,  row_1_start+LINE_HEIGHT, pos_column_1_end, row_1_start+LINE_HEIGHT), fill=GREY, width=1)
        draw.text((pos_column_1_center, row_2_start), 'БЛОКИ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_1_start, row_2_start + LINE_HEIGHT, pos_column_1_end, row_2_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        draw.text((pos_column_1_center, row_3_start), 'БРОСКИ МИМО ВОРОТ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_1_start, row_3_start + LINE_HEIGHT, pos_column_1_end, row_3_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        draw.text((pos_column_1_center, row_4_start), 'ПОТЕРИ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_1_start, row_4_start + LINE_HEIGHT, pos_column_1_end, row_4_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        draw.text((pos_column_2_center, row_1_start), 'ОТБОРЬ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_2_start, row_1_start + LINE_HEIGHT, pos_column_2_end, row_1_start + LINE_HEIGHT), fill=GREY, width=1)
        draw.text((pos_column_2_center, row_2_start), 'БРОСКИ В СТВОР', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_2_start, row_2_start + LINE_HEIGHT, pos_column_2_end, row_2_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        draw.text((pos_column_2_center, row_3_start), 'ПРОЦЕНТ РЕАЛИЗАЦИИ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_2_start, row_3_start + LINE_HEIGHT, pos_column_2_end, row_3_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        draw.text((pos_column_2_center, row_4_start), 'ШТРАФНЫЕ МИНУТЬ', font=kroftsmansm, fill=GREY, anchor="mm")
        draw.line((pos_column_2_start, row_4_start + LINE_HEIGHT, pos_column_2_end, row_4_start + LINE_HEIGHT), fill=GREY,
                  width=1)
        stats_1_row = row_1_start + LINE_HEIGHT
        stats_2_row = row_2_start + LINE_HEIGHT
        stats_3_row = row_3_start + LINE_HEIGHT
        stats_4_row = row_4_start + LINE_HEIGHT
        for teams in  stats_misc_parsed_hits_reduced:
            draw.text((pos_column_1_start + margin_horizontal, stats_1_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_1_end - margin_horizontal, stats_1_row + LINE_HEIGHT), str(teams['hits']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_1_row = stats_1_row + LINE_HEIGHT
        stats_1_row = row_1_start + LINE_HEIGHT
        for teams in  stats_misc_parsed_blocks_reduced:
            draw.text((pos_column_1_start + margin_horizontal, stats_2_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_1_end - margin_horizontal, stats_2_row + LINE_HEIGHT), str(teams['blockedShots']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_2_row = stats_2_row + LINE_HEIGHT
        stats_2_row = row_2_start + LINE_HEIGHT
        for teams in  stats_misc_parsed_missed_reduced:
            draw.text((pos_column_1_start + margin_horizontal, stats_3_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_1_end - margin_horizontal, stats_3_row + LINE_HEIGHT), str(teams['missedShots']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_3_row = stats_3_row + LINE_HEIGHT
        stats_3_row = row_3_start + LINE_HEIGHT
        for teams in  stats_misc_parsed_giveaways_reduced:
            draw.text((pos_column_1_start + margin_horizontal, stats_4_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_1_end - margin_horizontal, stats_4_row + LINE_HEIGHT), str(teams['giveaways']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_4_row = stats_4_row + LINE_HEIGHT
        stats_4_row = row_4_start + LINE_HEIGHT
        for teams in  stats_misc_parsed_takeaways_reduced:
            draw.text((pos_column_2_start + margin_horizontal, stats_1_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_2_end - margin_horizontal, stats_1_row + LINE_HEIGHT), str(teams['takeaways']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_1_row = stats_1_row + LINE_HEIGHT
        for teams in  stats_shots_parsed_shotsOnNet_reduced:
            draw.text((pos_column_2_start + margin_horizontal, stats_2_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_2_end - margin_horizontal, stats_2_row + LINE_HEIGHT), str(teams['shotsOnNet']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_2_row = stats_2_row + LINE_HEIGHT
        for teams in  stats_shots_parsed_shootingPct_reduced:
            draw.text((pos_column_2_start + margin_horizontal, stats_3_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_2_end - margin_horizontal, stats_3_row + LINE_HEIGHT), str(round(teams['shootingPct']*100,1)) + "%", font=def_font, fill=GREY,
                      anchor="rm")
            stats_3_row = stats_3_row + LINE_HEIGHT
        for teams in  stats_penalties_parsed_penaltyMinutes_reduced:
            draw.text((pos_column_2_start + margin_horizontal, stats_4_row + LINE_HEIGHT), teams['teamFullName'], font=def_font, fill=GREY, anchor="lm")
            draw.text((pos_column_2_end - margin_horizontal, stats_4_row + LINE_HEIGHT), str(teams['penaltyMinutes']), font=def_font, fill=GREY,
                      anchor="rm")
            stats_4_row = stats_4_row + LINE_HEIGHT
        draw.text((70, SCH-60), str(now_date), font=kroftsmansm, fill=GREY, anchor="lb")
        size = (167*4, 239*4)
        out = im.resize(size)
        out.show()
        filename = './rendered/out' + now_file + '_teams.png'
        out.save(filename)
        return filename

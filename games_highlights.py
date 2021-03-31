import jmespath
import requests
from datetime import datetime, timezone, timedelta
import argparse
import subprocess
from os.path import expanduser

import os

parser = argparse.ArgumentParser()
parser.add_argument("input_url")
now = datetime.today().strftime('%H:%M:%S')
now_file = datetime.today().strftime('%H%M%S')
now_date = datetime.today().strftime('%d.%m.%Y')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')

games_data = requests.get(
    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,broadcasts(all),game(content(media(epg)),seriesSummary),radioBroadcasts,metadata").json()

games_data_parsed = jmespath.search(
    "dates[].games[].{title: content.media.epg[?title=='Extended Highlights']|[0].items|[0].title, hl_id: content.media.epg[?title=='Extended Highlights']|[0].items|[0].id, date: content.media.epg[?title=='Extended Highlights']|[0].items|[0].date, status: status. detailedState}",
    games_data)
### YOUTUBE-DL SECTION ###
ydl = 'youtube-dl ' + '$1 -o "~/highlights/$opdate/%(title)s.%(ext)s" --restrict-filenames -f HTTP_CLOUD_MOBILE-221 --no-check-certificate'

for item in games_data_parsed:
    if item['status'] == "Final":
        subprocess.call(['~/highlights.sh ' + "https://www.nhl.com/video/c-" + item['hl_id']], shell=True)
    else:
        print(item['status'])

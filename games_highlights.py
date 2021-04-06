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
today = datetime.today().strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')

request_url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + today + "&hydrate=team,linescore,broadcasts(all),game(content(media(epg)),seriesSummary),radioBroadcasts,metadata"
print(request_url)
games_data = requests.get(request_url).json()

games_data_existanse = jmespath.search(
    "dates[].games[].{away: teams.away.team.abbreviation, home: teams.home.team.abbreviation, title: content.media.epg[?title=='Extended Highlights']|[0].items|[0].title, hl_id: content.media.epg[?title=='Extended Highlights']|[0].items|[0].id, date: content.media.epg[?title=='Extended Highlights']|[0].items|[0].date, status: status. detailedState}",
    games_data)

games_data_parsed = jmespath.search(
    "dates[].games[].{away: teams.away.team.abbreviation, home: teams.home.team.abbreviation, title: content.media.epg[?title=='Extended Highlights']|[0].items|[0].title, hl_id: content.media.epg[?title=='Extended Highlights']|[0].items|[0].id, date: content.media.epg[?title=='Extended Highlights']|[0].items|[0].date, status: status. detailedState}",
    games_data)

for item in games_data_parsed:
    if item['hl_id']:
        #subprocess.call(['~/highlights.sh ' + "https://www.nhl.com/video/c-" + item['hl_id']], shell=True)
        subprocess.call(['~/highlights/' + today + '.list << ' + "https://www.nhl.com/video/c-" + item['hl_id']], shell=True)
        print(item['title'] + ", " + item['status'] + " https://www.nhl.com/video/c-" + item['hl_id'])
    else:
        print("! " + item['away'] + " @ " + item['home'] + ", " + item['status'] + str(len(games_data_parsed)))
        break

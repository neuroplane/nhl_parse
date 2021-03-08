from datetime import datetime, timedelta

import jmespath
import requests

yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

last_games = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate="+yesterday+"&endDate="+yesterday+"&hydrate=team,linescore,broadcasts(all),tickets,game(content(media(epg)),seriesSummary),radioBroadcasts,metadata,seriesSummary(series)&site=ru_nhl&teamId=&gameType=&timecode=").json()
last_games_parsed = jmespath.search("dates[].games[].teams[].{away: {team: away.team.teamName, "
                                    "loc: away.team.locationName, score: away.score},home:{team: home.team.teamName, "
                                    "loc: home.team.locationName, score: home.score}}", last_games)

print(last_games_parsed)
for item in last_games_parsed:
    print(item['away']['loc'] + " " + item['away']['team'] + " " + str(item['away']['score']) + ":" + str(item['home']['score']) + " " + item['home']['loc'] + " " + item['home']['team'])
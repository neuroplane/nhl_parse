import jmespath
import requests

games_data = requests.get(
    "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2021-03-29&endDate=2021-03-29&hydrate=team,linescore,broadcasts(all),game(content(media(epg)),seriesSummary),radioBroadcasts,metadata").json()

games_data_parsed = jmespath.search(
    "dates[].games[].{title: content.media.epg[?title=='Extended Highlights']|[0].items|[0].title, hl_id: content.media.epg[?title=='Extended Highlights']|[0].items|[0].id, date: content.media.epg[?title=='Extended Highlights']|[0].items|[0].date, status: status. detailedState}",
    games_data)

print(games_data_parsed)
n = 1
for index, item in zip(range(10), games_data_parsed):
    print(str(n) + ". " + item['title'] + ", https://www.nhl.com/video/c-" + item['hl_id'] + ", " + item['date'] + ", " + item['status'])
    n = n + 1

import json

import requests
import jmespath
import time
import random

start_year = 2021
end_year = 2022
p = None
dataTypes = ['summary', 'bio']

bios_url = "https://api.nhle.com/stats/rest/en/skater/bios?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
goalsForAgainst_url = "https://api.nhle.com/stats/rest/en/skater/goalsForAgainst?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22evenStrengthGoalDifference%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
summary_url = "https://api.nhle.com/stats/rest/ru/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start=0&limit=10&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
total_skaters = requests.get(summary_url).json()
total_skaters_number = jmespath.search("total", total_skaters)

pages = total_skaters_number//100
total_field_players = []
total_goals_for_against = []
bios = []

time.sleep(random.randrange(1, 5))
'''
# GET ALL FIELD PLAYERS ######################################################
for page in range(0,total_skaters_number//100+1):
    p = page*100
    print(str(p) + " ::: SUMMARY")
    page_url = "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    field_list_en = jmespath.search("data[].{playerId: playerId, last_name_en: lastName, full_name_en: skaterFullName}", page_result)
    for item in range(len(field_list_en)):
        total_field_players.append(field_list_en[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/inputdata"
payload_prepared = {"items": total_field_players}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
'''
# SUMMARY ######################################################
for page in range(0, total_skaters_number//100+1):
    p = page*100
    print(str(p) + " ::: SUMMARY")
    page_url = "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    field_list = jmespath.search("data[]", page_result)
    for item in range(len(field_list)):
        total_field_players.append(field_list[item])
    time.sleep(random.randrange(1, 2))

url = "https://x125.ru/api/nhle/summary"
payload_prepared = {"items": total_field_players}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
'''
#GFA ##########################################################
for page in range(0,total_skaters_number//100+1):
    p = page*100
    print(str(p) + " ::: GOALS FOR AND AGAINST")
    page_url = "https://api.nhle.com/stats/rest/en/skater/goalsForAgainst?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22evenStrengthGoalDifference%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    goals_for_against_list = jmespath.search("data[]", page_result)
    for item in range(len(goals_for_against_list)):
        total_goals_for_against.append(goals_for_against_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/goalsforagainst"
payload_prepared = {"items": total_goals_for_against}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
#BIOS ##########################################################
for page in range(0,total_skaters_number//100+1):
    p = page*100
    print(str(p) + " ::: BIOS")
    page_url = "https://api.nhle.com/stats/rest/en/skater/bios?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    bios_list = jmespath.search("data[]", page_result)
    for item in range(len(bios_list)):
        bios.append(bios_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/bios"
payload_prepared = {"items": bios}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# FACEOFFPERCENTAGES ##########################################################
faceoffpercentages = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: FACEOFFPERCENTAGES")
    page_url = "https://api.nhle.com/stats/rest/en/skater/faceoffpercentages?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    faceoffpercentages_list = jmespath.search('data[]', page_result)
    for item in range(len(faceoffpercentages_list)):
        faceoffpercentages.append(faceoffpercentages_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/faceoffpercentages"
payload_prepared = {"items": faceoffpercentages}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# FACEOFFWINS ##########################################################
faceoffwins = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: FACEOFFWINS")
    page_url = "https://api.nhle.com/stats/rest/en/skater/faceoffwins?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    faceoffwins_list = jmespath.search('data[]', page_result)
    for item in range(len(faceoffwins_list)):
        faceoffwins.append(faceoffwins_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/faceoffwins"
payload_prepared = {"items": faceoffwins}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# REALTIME ##########################################################
realtime = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: REALTIME")
    page_url = "https://api.nhle.com/stats/rest/en/skater/realtime?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    realtime_list = jmespath.search('data[]', page_result)
    for item in range(len(realtime_list)):
        realtime.append(realtime_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/realtime"
payload_prepared = {"items": realtime}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# PENALTIES ##########################################################
penalties = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: PENALTIES")
    page_url = "https://api.nhle.com/stats/rest/en/skater/penalties?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    penalties_list = jmespath.search('data[]', page_result)
    for item in range(len(penalties_list)):
        penalties.append(penalties_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/penalties"
payload_prepared = {"items": penalties}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# PENALTYKILL ##########################################################
penaltykill = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: PENALTYKILL")
    page_url = "https://api.nhle.com/stats/rest/en/skater/penaltykill?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    penaltykill_list = jmespath.search('data[]', page_result)
    for item in range(len(penaltykill_list)):
        penaltykill.append(penaltykill_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/penaltykill"
payload_prepared = {"items": penaltykill}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# POWERPLAY ##########################################################
powerplay = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: POWERPLAY")
    page_url = "https://api.nhle.com/stats/rest/en/skater/powerplay?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    powerplay_list = jmespath.search('data[]', page_result)
    for item in range(len(powerplay_list)):
        powerplay.append(powerplay_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/powerplay"
payload_prepared = {"items": powerplay}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# PUCKPOSSESIONS ########################################################## NOT WORKING FOR THE TIME !!!!!!!
puckpossesions = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: PUCKPOSSESIONS")
    page_url = "https://api.nhle.com/stats/rest/en/skater/puckPossessions?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22satPct%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    puckpossesions_list = jmespath.search('data[]', page_result)
    for item in range(len(puckpossesions_list)):
        puckpossesions.append(puckpossesions_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/puckpossesions"
payload_prepared = {"items": puckpossesions}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# SUMMARYSHOOTING ##########################################################
summaryshooting = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: SUMMARYSHOOTING")
    page_url = "https://api.nhle.com/stats/rest/en/skater/summaryshooting?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    summaryshooting_list = jmespath.search('data[]', page_result)
    for item in range(len(summaryshooting_list)):
        summaryshooting.append(summaryshooting_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/summaryshooting"
payload_prepared = {"items": summaryshooting}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# PERCENTAGES ##########################################################
percentages = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: PERCENTAGES")
    page_url = "https://api.nhle.com/stats/rest/en/skater/percentages?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    percentages_list = jmespath.search('data[]', page_result)
    for item in range(len(percentages_list)):
        percentages.append(percentages_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/percentages"
payload_prepared = {"items": percentages}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# SCORINGRATES ##########################################################
scoringrates = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: SCORINGRATES")
    page_url = "https://api.nhle.com/stats/rest/en/skater/scoringRates?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22pointsPer605v5%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goalsPer605v5%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    scoringrates_list = jmespath.search('data[]', page_result)
    for item in range(len(scoringrates_list)):
        scoringrates.append(scoringrates_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/scoringrates"
payload_prepared = {"items": scoringrates}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# SCORINGPERGAME ##########################################################
scoringpergame = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: SCORINGPERGAME")
    page_url = "https://api.nhle.com/stats/rest/en/skater/scoringpergame?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    scoringpergame_list = jmespath.search('data[]', page_result)
    for item in range(len(scoringpergame_list)):
        scoringpergame.append(scoringpergame_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/scoringpergame"
payload_prepared = {"items": scoringpergame}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)	
time.sleep(random.randrange(1, 5))
# SHOOTOUT ##########################################################
shootout = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: SHOOTOUT")
    page_url = "https://api.nhle.com/stats/rest/en/skater/shootout?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22shootoutGoals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=50&factCayenneExp=&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    shootout_list = jmespath.search('data[]', page_result)
    for item in range(len(shootout_list)):
        shootout.append(shootout_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/shootout"
payload_prepared = {"items": shootout}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# SHOTTYPE ##########################################################
shottype = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: SHOTTYPE")
    page_url = "https://api.nhle.com/stats/rest/en/skater/shottype?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22shots%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22shootingPct%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    shottype_list = jmespath.search('data[]', page_result)
    for item in range(len(shottype_list)):
        shottype.append(shottype_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/shottype"
payload_prepared = {"items": shottype}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
time.sleep(random.randrange(1, 5))
# TIMEONICE ##########################################################
timeonice = []
for page in range(0, total_skaters_number // 100 + 1):
    p = page * 100
    print(str(p) + " ::: TIMEONICE")
    page_url = "https://api.nhle.com/stats/rest/en/skater/timeonice?isAggregate=false&isGame=false&start=" + str(
        p) + "&limit=1000&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    timeonice_list = jmespath.search('data[]', page_result)
    for item in range(len(timeonice_list)):
        timeonice.append(timeonice_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/timeonice"
payload_prepared = {"items": timeonice}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)
'''

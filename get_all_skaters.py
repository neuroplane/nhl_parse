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

'''
#SUMMARY######################################################
for page in range(0,total_skaters_number//100+1):
    p = page*100
    print(str(p) + " ::: SUMMARY")
    page_url = "https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start="+str(p)+"&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20212022%20and%20seasonId%3E=20212022"
    page_result = requests.get(page_url).json()
    field_list = jmespath.search("data[]", page_result)
    for item in range(len(field_list)):
        total_field_players.append(field_list[item])
    time.sleep(random.randrange(1, 5))

url = "https://x125.ru/api/nhle/inputdata"
payload_prepared = {"items": total_field_players}
payload = json.dumps(payload_prepared)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, data=payload, headers=headers)

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
'''
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


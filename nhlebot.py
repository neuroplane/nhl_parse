# import os

import requests
# import json
# import keyboard

import jmespath
import requests
import pytz
import datetime as dt

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
# from aiogram.types import InputFile
from aiogram.types import message
from aiogram.utils import executor
from aiogram.utils.payload import generate_payload
from aiogram.types import FSInputFile


from datetime import datetime, timezone, timedelta
##########################################################
msk = pytz.timezone("Europe/Moscow")
now = datetime.today().strftime('%H:%M:%S')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')
before_yesterday = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
##########################################################


TOKEN = '2100506147:AAGI7UjsKpUcIkkvO36Ix5O0Z3DXEXSBgOk'  # токен бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)  # класс бота, через него основные команды
dp = Dispatcher(bot)  # класс диспатчера, через него работают декораторы, то есть ловятся сообщения
#dbtoken = "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
#apiheaders = {"Content-Type": "application/json", "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"}
#apiurl = "https://x125.ru/api/neurotlg/"
#schoolapiurl = "https://x125.ru/api/public/"
#family = (requests.request("POST", apiurl + 'getfamily', headers=apiheaders)).json()
#drive_url = "https://drive.google.com/uc?id="

json_scores = []

class elitebot:
    @staticmethod
    def get_scores():  # первая функция
        print("FUNCTION HAS BEEN CALLED")
        json_score = requests.get(
            "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + today + "&hydrate=team,linescore,game(content(media(epg)))").json()
        json_scores = jmespath.search(
            "dates[].{Date: date, Games: games[].{date:gameDate, GameState: linescore.currentPeriod, AwayScore: teams.away.score, HomeScore: teams.home.score, Home: teams.home.team.abbreviation, Away:teams.away.team.abbreviation}}",
            json_score)
        print(json_scores)

def isallowed(user_id):
    users = [77717804, 391371524, 358938845, 108769960, 878143763]
    return user_id in users


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Что это за бот?"),
        types.BotCommand("help", "Краткое описание что это за бот."),
        types.BotCommand("whoami", "who ami i"),
        types.BotCommand("check", "user check"),
        types.BotCommand("latest_scores", "Последний игровой день"),
        types.BotCommand("top_points", "Топ-10 бомбардиров"),
        types.BotCommand("top_missed", "Мазилы дня")
    ])


@dp.message_handler(commands=['start', 'help'])  # ловим команды в сообщениях
async def start_help(message: types.Message):
    if isallowed(message.from_user.id):
        await message.answer("Всё заебок")
        print("USER: " + message.from_user.username + "\n" + "REQUEST: " + message.text + " ALLOWED")
    else:
        await message.reply("Нет авторизации для user id " + str(message.from_user.id))
        print("USER: " + message.from_user.username + " ID: " + str(message.from_user.id) +"\n" + "REQUEST: " + message.text + " DISALLOWED")

@dp.message_handler(commands="check")
async def user_check(message: types.Message):
    user_allowed = isallowed(message.from_user.id)
    await message.answer(user_allowed)

@dp.message_handler(commands="whoami")
async def whoami(message: types.Message):
    await message.answer("user id: <code>" + str(message.from_user.id) + "</code>")
    print(message.chat.id)
    print(message)
    # await bot.send_video(chat_id= -1001790212138, width=640, height=360, video=open('9462532.mp4', 'rb'), supports_streaming=True)


@dp.message_handler(commands="latest_scores")
async def latest_scores(message: types.Message):
    json_score = requests.get(
        "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + today + "&hydrate=team,linescore,game(content(media(epg)))").json()
    json_scores = jmespath.search(
        "dates[].{Date: date, Games: games[].{date:gameDate, Details: status.detailedState, GameState: linescore.currentPeriod, AwayScore: teams.away.score, HomeScore: teams.home.score, Home: teams.home.team.abbreviation, Away:teams.away.team.abbreviation}}",
        json_score)
    latest = ""
    future = ""
    postponed = ""
    for item in json_scores:
        for game in item['Games']:
            if game['GameState'] == 3:
                Gamestate = ''
                latest = latest + game['Away'] + " " + str(game['AwayScore']) + ":" + str(game['HomeScore']) + " " + \
                         game['Home'] + "" + Gamestate + "\n"
            elif game['GameState'] == 4:
                Gamestate = ' OT'
                latest = latest + game['Away'] + " " + str(game['AwayScore']) + ":" + str(game['HomeScore']) + " " + \
                         game['Home'] + "" + Gamestate + "\n"
            elif game['GameState'] == 5:
                Gamestate = ' SO'
                latest = latest + game['Away'] + " " + str(game['AwayScore']) + ":" + str(game['HomeScore']) + " " + \
                         game['Home'] + "" + Gamestate + "\n"
            else:
                if game['Details'] == 'Postponed':
                    Gamestate = 'Перенесён'
                    future = future + game['Away'] + " @ " + game['Home'] + "" + " : " + Gamestate + "\n"
                else:
                    actualDate = datetime.strptime(game['date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                    future = future + game['Away'] + " @ "  + game['Home'] + "" + Gamestate + " : " + actualDate.astimezone(msk).strftime("%H:%M") + "\n"

    print("USER: " + message.from_user.username + "\n" + "REQUEST: " + message.text)
    await message.delete()
    await message.answer(text="Матчи за " + yesterday_rus + ":\n" + "`" + latest + "`" + "\nСегодня ночью (по Москве):" + "\n" +  "`" + future + "`", parse_mode=types.ParseMode.MARKDOWN)
#######################################################################
@dp.message_handler(commands="top_points")
async def latest_scores(message: types.Message):
    url = "https://x125.ru/api/nhle/getpoints"

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
    }

    response = requests.request("POST", url, json=payload, headers=headers).json()
    json_list = ""
    namelengths = []

    for player in response:
        namelengths.append(len(player['lastname']))
    skatermaxlength = max(namelengths)
    for player in response:
        spaces = skatermaxlength - len(player['lastname'])
        json_list = json_list + player['lastname'] + ' '*(spaces +2) + str(player['points']) + "\n"
    print("USER: " + message.from_user.username + " :: " + "REQUEST: " + message.text)
    await message.delete()
    await message.answer("Бомбардиры: \n" + "`" + json_list + "`", parse_mode=types.ParseMode.MARKDOWN)
######
@dp.message_handler(commands="top_missed")
async def latest_scores(message: types.Message):
    stat = ""
    miss_url = "https://api.nhle.com/stats/rest/en/skater/realtime?isAggregate=true&isGame=true&sort=%5B%7B%22property%22:%22missedShots%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22playerId%22,%22direction%22:%22ASC%22%7D%5D&start=0&limit=15&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameDate%3C=%22"+yesterday+"%2023%3A59%3A59%22%20and%20gameDate%3E=%22"+yesterday+"%22%20and%20gameTypeId=2"
    response = requests.get(miss_url).json()
    json_missed = jmespath.search("data[].{lastname: lastName, misses: missedShots}", response)
    namelengths = []
    json_list = ""
    print(response)
    for player in json_missed:
        namelengths.append(len(player['lastname']))
    skatermaxlength = max(namelengths)
    for player in json_missed:
        spaces = skatermaxlength - len(player['lastname'])
        json_list = json_list + player['lastname'] + ' ' * (spaces + 2) + str(player['misses']) + "\n"
    await message.delete()
    await message.answer("Мазилы дня: \n" + "`" + json_list + "`", parse_mode=types.ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands)  # начало поллинга

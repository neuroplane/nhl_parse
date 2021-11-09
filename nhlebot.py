# import os

import requests
# import json
# import keyboard

import jmespath
import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
# from aiogram.types import InputFile
from aiogram.types import message
from aiogram.utils import executor
from aiogram.utils.payload import generate_payload

from datetime import datetime, timezone, timedelta
##########################################################
now = datetime.today().strftime('%H:%M:%S')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
before_yesterday = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
yesterday_rus = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
##########################################################


TOKEN = '2100506147:AAEbTO4s9eP_kLCFVtoSSjhDnkE-ES7YQR4'  # токен бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)  # класс бота, через него основные команды
dp = Dispatcher(bot)  # класс диспатчера, через него работают декораторы, то есть ловятся сообщения
#dbtoken = "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
#apiheaders = {"Content-Type": "application/json", "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"}
#apiurl = "https://x125.ru/api/neurotlg/"
#schoolapiurl = "https://x125.ru/api/public/"
#family = (requests.request("POST", apiurl + 'getfamily', headers=apiheaders)).json()
#drive_url = "https://drive.google.com/uc?id="

json_scores = None

class elitebot:
    @staticmethod
    def get_scores():  # первая функция
        print("FUNCTION HAS BEEN CALLED")
        json_score = requests.get(
            "https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + yesterday + "&endDate=" + yesterday + "&hydrate=team,linescore,game(content(media(epg)))").json()
        json_scores = jmespath.search(
            "dates[].{Date: date, Games: games[].{date:gameDate, GameState: linescore.currentPeriod, AwayScore: teams.away.score, HomeScore: teams.home.score, Home: teams.home.team.abbreviation, Away:teams.away.team.abbreviation}}",
            json_score)
        print(json_scores)

def isallowed(user_id):
    users = [77717804, 391371524]
    return user_id in users


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Что это за бот?"),
        types.BotCommand("help", "Краткое описание что это за бот."),
        types.BotCommand("whoami", "who ami i"),
        types.BotCommand("check", "user check"),
        types.BotCommand("latest_scores", "Последний игровой день")
    ])


@dp.message_handler(commands=['start', 'help'])  # ловим команды в сообщениях
async def start_help(message: types.Message):
    if isallowed(message.from_user.id):
        await message.answer("Всё заебок")
    else:
        await message.reply("Нет авторизации для user id " + str(message.from_user.id))

@dp.message_handler(commands="check")
async def user_check(message: types.Message):
    user_allowed = isallowed(message.from_user.id)
    await message.answer(user_allowed)

@dp.message_handler(commands="whoami")
async def whoami(message: types.Message):
    await message.answer("user id: <code>" + str(message.from_user.id) + "</code>")
    print(message.chat.id)
    print(message)


@dp.message_handler(commands="latest_scores")
async def latest_scores(message: types.Message):
    elitebot.get_scores()
    await message.delete()
    await bot.send_message(chat_id=-713521144, text=str(json_scores),
                           parse_mode=types.ParseMode.MARKDOWN)

@dp.channel_post_handler(chat_id=-1001790212138)
async def channel_id(post: types.Message):
    await post.delete()
    await post.answer("Channel id: " + str(post.sender_chat.id) + ", " + post.sender_chat.title + " (" + post.text + ")")
    print(post)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_default_commands)  # начало поллинга

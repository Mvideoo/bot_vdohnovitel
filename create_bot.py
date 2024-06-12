from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import sqlite3 as sq

TOKEN = '7428844445:AAHxzrlbZUJTxOR4BMGgPnzuWr-OrdjmjCU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


base = sq.connect("humans.db")
cur = base.cursor()
if base:
    print("connected")

base2 = sq.connect(('links.db'))
cur2 = base2.cursor()
base2.execute('CREATE TABLE IF NOT EXISTS links(link)')

base.execute(
    'CREATE TABLE IF NOT EXISTS humans(id PRIMARY KEY, name, technician, bio_chemical, social_economy, language, result, tokens, chanels, mastermind_message, test, passing_test, answer, config_choice, newsletter, org1, org2, org3, org4, rul1, rul2, rul3, rul4, comm1, comm2, comm3, comm4, an1, an2, an3)')
base.commit()

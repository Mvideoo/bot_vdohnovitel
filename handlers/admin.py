import asyncio

import aioschedule
from aiogram import types, Dispatcher
import random
from create_bot import bot, dp, base, cur, cur2, base2
from keyboards import *
import logging
from data_base.sent import sentences
from admins_id import admin_id
from data_base.channels import all_channels


async def start_mailing():
    cur.execute("SELECT id FROM humans")
    user_ids = [row[0] for row in cur.fetchall()]
    message_text = random.choice(sentences)

    for user_id in user_ids:
        try:
            if int(cur.execute('SELECT mastermind_message FROM humans WHERE id == ?', (int(user_id),)).fetchone()[
                       0]) == 1:
                await bot.send_message(user_id, message_text)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")


async def scheduler():
    aioschedule.every().day.at("12:00").do(start_mailing())
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@dp.message_handler(commands=["mailing"])
async def mailing(message):
    if message.from_user.id in admin_id:
        await message.answer("Начинаю рассылку...")
        await start_mailing()
        await message.answer("Рассылка завершена.")
    else:
        await message.answer("У вас нет разрешения на выполнение этой команды.")


@dp.message_handler(commands=["help_for_admins"])
async def mailing(message):
    if message.from_user.id in admin_id:
        await message.answer(f"Команды админа: \n"
                             f"/mailing - рассылка вдохновляющих сообщений (после одной рассылки они будут рассылаться автоматически каждый день в то же время) \n"
                             f"/all_names - список всех пользователей бота \n"
                             f"/task_from_user <user_name> все задания нужного пользователя, пример пользования: /task_from_user user123, имя берется из /all_names \n"
                             f"/оценка_<номер задания><тип задания> <имя пользователя> <балл> - поставить оценку за задачу пользователя, пример пользования: /оценка_2анализ user321 85, максимальное колво баллов за задачу - 100\n"
                             f"/update_list <ссылка на сообщество> - обновить список сообществ, которые могут быть интересны пользователям")


@dp.message_handler(commands=["all_names"])
async def mailing(message):
    cur.execute("SELECT name FROM humans")
    user_names = [str(row[0]) for row in cur.fetchall()]
    await bot.send_message(message.from_user.id, '\n'.join(user_names))


@dp.message_handler(commands=["update_list"])
async def mailing(message):
    message_text = message.text[len("/update_list"):].strip()
    cur2.execute(
        'INSERT INTO links VALUES(?)',(message_text, ))
    base2.commit()
    await bot.send_message(message.from_user.id, 'список обновлен')


@dp.message_handler(commands=["task_from_user"])
async def broadcast_message_to_all_users(message: types.Message):
    if message.from_user.id in admin_id:

        message_text = message.text[len("/task_from_users"):].strip()

        try:
            org1 = cur.execute('SELECT org1 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            org2 = cur.execute('SELECT org2 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            org3 = cur.execute('SELECT org3 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            org4 = cur.execute('SELECT org4 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]

            rul1 = cur.execute('SELECT rul1 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            rul2 = cur.execute('SELECT rul2 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            rul3 = cur.execute('SELECT rul3 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            rul4 = cur.execute('SELECT rul4 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]

            comm1 = cur.execute('SELECT comm1 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            comm2 = cur.execute('SELECT comm2 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            comm3 = cur.execute('SELECT comm3 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            comm4 = cur.execute('SELECT comm4 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]

            an1 = cur.execute('SELECT an1 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            an2 = cur.execute('SELECT an2 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]
            an3 = cur.execute('SELECT an3 FROM humans WHERE name == ?', (str(message_text),)).fetchone()[0]

            await bot.send_message(message.from_user.id, f'организания \n {org1} \n {org2} \n {org3} \n {org4}')
            await bot.send_message(message.from_user.id, f'управление\n {rul1} \n {rul2} \n {rul3} \n {rul4}')
            await bot.send_message(message.from_user.id, f'коммуникации\n {comm1} \n {comm2} \n {comm3} \n {comm4}')
            await bot.send_message(message.from_user.id, f'анализ\n {an1} \n {an2} \n {an3}')
            await bot.send_message(message.from_user.id,
                                   f'если вы хотите поставить баллы за задачу пользователя, отправьте сообщение "/оценка_<номер задачи><вид задачи> <имя пользователя> <балл>" \n пример: "/оценка_2коммуникации user228 75 \n всего можно поставить 100 баллов за задание')
        except Exception as e:
            logging.error(f"Ошибка: {e}")


@dp.message_handler(commands=['update_leaderboard'])
async def update_leaderboard(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer("Обновление лидерборда...")

        leaderboard_text = "Лидерборд пользователей:\n"

        cur.execute("SELECT name, tokens FROM humans ORDER BY tokens DESC")
        position = 1
        for row in cur.fetchall():
            name, token = row
            leaderboard_text += f"{position}. {name} - {token} points\n"
            position += 1

        await message.answer(leaderboard_text)


@dp.message_handler(commands=["оценка_1планирование"])
async def command_t1org(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_1планирование"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET org1 == ? WHERE name == ?', (str(
                cur.execute('SELECT org1 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 1 задание из планирования, посмотреть - /мое_задание_1планирование')


@dp.message_handler(commands=["оценка_2планирование"])
async def command_t2org(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/2оценка_планирование"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET org2 == ? WHERE name == ?', (str(
                cur.execute('SELECT org2 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 2 задание из планирования, посмотреть - /мое_задание_2планирование')


@dp.message_handler(commands=["оценка_3планирование"])
async def command_t3org(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/3оценка_планирование"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET org3 == ? WHERE name == ?', (str(
                cur.execute('SELECT org3 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 3 задание из планирования, посмотреть - /мое_задание_3планирование')


@dp.message_handler(commands=["оценка_4планирование"])
async def command_t4org(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_4планирование"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET org4 == ? WHERE name == ?', (str(
                cur.execute('SELECT org4 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 4 задание из планирования, посмотреть - /мое_задание_4планирование')


@dp.message_handler(commands=["оценка_1управление"])
async def command_t1rul(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_1управление"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET rul1 == ? WHERE name == ?', (str(
                cur.execute('SELECT rul1 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 1 задание из управления, посмотреть - /мое_задание_1управление')


@dp.message_handler(commands=["оценка_2управление"])
async def command_t2rul(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_2управление"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET rul2 == ? WHERE name == ?', (str(
                cur.execute('SELECT rul2 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 2 задание из управления, посмотреть - /мое_задание_2управление')


@dp.message_handler(commands=["оценка_3управление"])
async def command_t3rul(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_3управление"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET rul3 == ? WHERE name == ?', (str(
                cur.execute('SELECT rul3 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 3 задание из управления, посмотреть - /мое_задание_3управление')


@dp.message_handler(commands=["оценка_4управление"])
async def command_t4rul(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_4управление"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET rul4 == ? WHERE name == ?', (str(
                cur.execute('SELECT rul4 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 4 задание из управления, посмотреть - /мое_задание_4управление')


@dp.message_handler(commands=["оценка_1коммуникации"])
async def command_t1comm(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_1коммуникации"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET comm1 == ? WHERE name == ?', (str(
                cur.execute('SELECT comm1 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 1 задание из коммуникаций, посмотреть - /мое_задание_1коммуникации')


@dp.message_handler(commands=["оценка_2коммуникации"])
async def command_t2comm(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_2коммуникации"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET comm2 == ? WHERE name == ?', (str(
                cur.execute('SELECT comm2 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 2 задание из коммуникаций, посмотреть - /мое_задание_2коммуникации')


@dp.message_handler(commands=["оценка_3коммуникации"])
async def command_t3comm(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("оценка_/3коммуникации"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET comm3 == ? WHERE name == ?', (str(
                cur.execute('SELECT comm3 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 3 задание из коммуникаций, посмотреть - /мое_задание_3коммуникации')


@dp.message_handler(commands=["оценка_4коммуникации"])
async def command_t4comm(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_4коммуникации"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET comm4 == ? WHERE name == ?', (str(
                cur.execute('SELECT comm4 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 4 задание из коммуникаций, посмотреть - /мое_задание_4коммуникации')


@dp.message_handler(commands=["оценка_1анализ"])
async def command_t1an(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_1анализ"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET an1 == ? WHERE name == ?', (str(
                cur.execute('SELECT an1 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 1 задание из анализа, посмотреть - /мое_задание_1анализ')


@dp.message_handler(commands=["оценка_2анализ"])
async def command_t2an(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_2анализ"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET an2 == ? WHERE name == ?', (str(
                cur.execute('SELECT an2 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 2 задание из анализа, посмотреть - /мое_задание_2анализ')


@dp.message_handler(commands=["оценка_3анализ"])
async def command_t3an(message: types.Message):
    if message.from_user.id in admin_id:
        message_text = message.text[len("/оценка_3анализ"):].strip()
        us_name, token = message_text.split()
        if int(token) > 100:
            await message.answer('за задание нельзя ставить более 100 баллов!')
        else:
            cur.execute("UPDATE humans SET tokens == ? WHERE name ==?", (
                int(cur.execute('SELECT tokens FROM humans WHERE name == ?', (str(us_name),)).fetchone()[0]) + int(
                    token),
                str(us_name)))
            base.commit()
            cur.execute('UPDATE humans SET an3 == ? WHERE name == ?', (str(
                cur.execute('SELECT an3 FROM humans WHERE name == ?', (str(us_name),)).fetchone()[
                    0]) + f'\n оценка: {token}', str(us_name)))
            base.commit()
            await bot.send_message(message.from_user.id, 'оценка выставлена')
            await bot.send_message(int(cur.execute('SELECT id FROM humans WHERE name == ?', (us_name,)).fetchone()[0]),
                                   'вам выставлена новая оценка за 3 задание из анализа, посмотреть - /мое_задание_2анализ')


async def on_startup(_):
    asyncio.create_task(scheduler())


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(mailing, commands=['mailing'])
    dp.register_message_handler(broadcast_message_to_all_users, commands=['task_from_users'])

    dp.register_message_handler(command_t1org, commands=['оценка_1планирование'])
    dp.register_message_handler(command_t2org, commands=['оценка_2планирование'])
    dp.register_message_handler(command_t3org, commands=['оценка_3планирование'])
    dp.register_message_handler(command_t4org, commands=['оценка_4планирование'])

    dp.register_message_handler(command_t1rul, commands=['оценка_1управление'])
    dp.register_message_handler(command_t2rul, commands=['оценка_2управление'])
    dp.register_message_handler(command_t3rul, commands=['оценка_3управление'])
    dp.register_message_handler(command_t4rul, commands=['оценка_4управление'])

    dp.register_message_handler(command_t1comm, commands=['оценка_1коммуникации'])
    dp.register_message_handler(command_t2comm, commands=['оценка_2коммуникации'])
    dp.register_message_handler(command_t3comm, commands=['оценка_3коммуникации'])
    dp.register_message_handler(command_t4comm, commands=['оценка_4коммуникации'])

    dp.register_message_handler(command_t1an, commands=['оценка_1анализ'])
    dp.register_message_handler(command_t2an, commands=['оценка_2анализ'])
    dp.register_message_handler(command_t3an, commands=['оценка_3анализ'])

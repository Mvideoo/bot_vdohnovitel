from aiogram import types, Dispatcher
from create_bot import bot, dp, base, cur, cur2
from keyboards.client_kb import kb_client, kb_client_2, kb_client_3
from data_base.tests import x
from admins_id import admin_id
from data_base.task import xx


@dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "привет! Это бот - вдохновитель! Я помогу тебе разобраться в своем направлении, а также подкину интересных задач, благодаря которым ты сможешь улучшать свой профиль\n Давай сначала пройдем тест, в нем всего 19 вопросов - /test",
                           reply_markup=kb_client)
    if message.from_user.id in admin_id:
        await bot.send_message(message.from_user.id,
                               'вы зарегистрированы как админ, команды админа на /help_for_admins')
    cur.execute(
        'INSERT INTO humans VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (int(message.from_user.id), message.from_user.username, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 'none', 'none',
         'none', 'none', 'none', 'none',
         'none', 'none', 'none',
         'none', 'none', 'none', 'none', 'none', 'none'))
    base.commit()


@dp.message_handler(commands=["tasks"])
async def command_tasks(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'выбирай задание, которое хочешь решить, когда решишь его, отправляй результат, но в начале напиши номер задания и его вид со слэшем\n пример: "/2анализ <решение>"\n'
                           'чтобы посмотреть свое решение на задачу - пиши /мое_задание_<номер задания><вид задания>, пример: /мое_задание_2управление',
                           reply_markup=kb_client_3)


@dp.message_handler(commands=["list"])
async def command_list(message: types.Message):
    await bot.send_message(message.from_user.id, "списки с интересными каналами")
    await bot.send_message(message.from_user.id, '\n'.join([i for i in cur2.execute('SELECT link FROM links').fetchone()]))

@dp.message_handler(commands=["profile"])
async def command_profile(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f"у тебя {cur.execute('SELECT tokens FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]} баллов")


@dp.message_handler(commands=['top_1'])
async def my_rating(message: types.Message):
    leaderboard_text = "Топ-1 пользователь:\n"
    cur.execute("SELECT id, name, tokens FROM humans ORDER BY tokens DESC LIMIT 1")
    position = 1
    user_id, first_name, points = cur.fetchone()
    leaderboard_text += f"{position}. {first_name} - {points} баллов"
    await bot.send_message(message.from_user.id, leaderboard_text)

@dp.message_handler(commands=["test"])
async def command_test(message: types.Message):
    id = message.from_user.id
    if int(cur.execute('SELECT passing_test FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == 0:
        cur.execute('UPDATE humans SET passing_test == ? WHERE id == ?', (1, message.from_user.id))
        base.commit()
        cur.execute('UPDATE humans SET technician == ? WHERE id == ?', (1, id))
        base.commit()
        cur.execute('UPDATE humans SET bio_chemical == ? WHERE id == ?', (1, id))
        base.commit()
        cur.execute('UPDATE humans SET social_economy == ? WHERE id == ?', (1, id))
        base.commit()
        cur.execute('UPDATE humans SET language == ? WHERE id == ?', (1, id))
        base.commit()
        cur.execute('UPDATE humans SET result == ? WHERE id == ?', (0, id))
        base.commit()
        cur.execute('UPDATE humans SET result == ? WHERE id == ?', (0, id))
        base.commit()
        await bot.send_message(message.from_user.id,
                               f"Давай начнем тест на твои сильные стороны!\nПиши номер ответа, который тебе понравился")
        cur.execute('UPDATE humans SET test == ? WHERE id == ?', (1, int(message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id, '\n'.join(x[0]))
    else:
        await bot.send_message(message.from_user.id, 'тест уже идет')


@dp.message_handler(commands=["config"])
async def command_configurations(message: types.Message):
    if cur.execute('SELECT mastermind_message FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
        0] == 1:
        await bot.send_message(message.from_user.id, f"Хочешь отписаться от расслыки вдохновляющих сообщений?",
                               reply_markup=kb_client_2)
    elif cur.execute('SELECT mastermind_message FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
        0] == 0:
        await bot.send_message(message.from_user.id, f"Хочешь снова подписаться на вдохновляющие сообщения?",
                               reply_markup=kb_client_2)
    cur.execute('UPDATE humans SET config_choice == ? WHERE id == ?', (1, message.from_user.id))
    base.commit()


@dp.message_handler(commands=["1планирование"])
async def command_1org(message: types.Message):
    if str(cur.execute('SELECT org1 FROM humans WHERE id == ?', (int(message.from_user.id), )).fetchone()[0]) == 'none':
        message_text = message.text[len("/1планирование"):].strip()
        cur.execute("UPDATE humans SET org1 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["2планирование"])
async def command_2org(message: types.Message):
    if str(cur.execute('SELECT org2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/2планирование"):].strip()
        cur.execute("UPDATE humans SET org2 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["3планирование"])
async def command_3org(message: types.Message):
    if str(cur.execute('SELECT org3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/3планирование"):].strip()
        cur.execute("UPDATE humans SET org3 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["4планирование"])
async def command_4org(message: types.Message):
    if str(cur.execute('SELECT org4 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/4планирование"):].strip()
        cur.execute("UPDATE humans SET org4 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["1управление"])
async def command_1rul(message: types.Message):
    if str(cur.execute('SELECT rul1 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/1управление"):].strip()
        cur.execute("UPDATE humans SET rul1 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["2управление"])
async def command_2rul(message: types.Message):
    if str(cur.execute('SELECT rul2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/2управление"):].strip()
        cur.execute("UPDATE humans SET rul2 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["3управление"])
async def command_3rul(message: types.Message):
    if str(cur.execute('SELECT rul3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/3управление"):].strip()
        cur.execute("UPDATE humans SET rul3 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["4управление"])
async def command_4rul(message: types.Message):
    if str(cur.execute('SELECT rul4 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/4управление"):].strip()
        cur.execute("UPDATE humans SET rul4 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["1коммуникации"])
async def command_1comm(message: types.Message):
    if str(cur.execute('SELECT comm1 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/1коммуникации"):].strip()
        cur.execute("UPDATE humans SET comm1 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["2коммуникации"])
async def command_2comm(message: types.Message):
    if str(cur.execute('SELECT comm2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/2коммуникации"):].strip()
        cur.execute("UPDATE humans SET comm2 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["3коммуникации"])
async def command_3comm(message: types.Message):
    if str(cur.execute('SELECT comm3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/3коммуникации"):].strip()
        cur.execute("UPDATE humans SET comm3 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["4коммуникации"])
async def command_4comm(message: types.Message):
    if str(cur.execute('SELECT comm4 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/4коммуникации"):].strip()
        cur.execute("UPDATE humans SET comm4 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["1анализ"])
async def command_1an(message: types.Message):
    if str(cur.execute('SELECT an1 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/1анализ"):].strip()
        cur.execute("UPDATE humans SET an1 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')

@dp.message_handler(commands=["2анализ"])
async def command_2an(message: types.Message):
    if str(cur.execute('SELECT an2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/2анализ"):].strip()
        cur.execute("UPDATE humans SET an2 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')
@dp.message_handler(commands=["3анализ"])
async def command_3an(message: types.Message):
    if str(cur.execute('SELECT an3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 'none':
        message_text = message.text[len("/3анализ"):].strip()
        cur.execute("UPDATE humans SET an3 == ? WHERE id ==?", (message_text, (message.from_user.id)))
        base.commit()
        await bot.send_message(message.from_user.id,
                               'Задача отправлена на проверку, ее нельзя изменить')
    else:
        await bot.send_message(message.from_user.id,
                               'Вы уже отправили решение на это задание')


@dp.message_handler(commands=["мое_задание_1планирование"])
async def command_w1org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2планирование"])
async def command_w2org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3планирование"])
async def command_w3org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4планирование"])
async def command_w4org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1управление"])
async def command_w1rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2управление"])
async def command_w2rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3управление"])
async def command_w3rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4управление"])
async def command_w4rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1коммуникации"])
async def command_w1comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2коммуникации"])
async def command_w2comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3коммуникации"])
async def command_w3comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4коммуникации"])
async def command_w4comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1анализ"])
async def command_w1an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an1 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["мое_задание_2анализ"])
async def command_w2an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["мое_задание_3анализ"])
async def command_w3an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["мое_задание_1планирование"])
async def command_w1org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2планирование"])
async def command_w2org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3планирование"])
async def command_w3org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4планирование"])
async def command_w4org(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT org4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1управление"])
async def command_w1rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2управление"])
async def command_w2rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3управление"])
async def command_w3rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4управление"])
async def command_w4rul(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT rul4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1коммуникации"])
async def command_w1comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm1 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_2коммуникации"])
async def command_w2comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm2 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_3коммуникации"])
async def command_w3comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm3 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_4коммуникации"])
async def command_w4comm(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT comm4 FROM humans WHERE id == ?',
                                       (int(message.from_user.id),)).fetchone()[0])


@dp.message_handler(commands=["мое_задание_1анализ"])
async def command_w1an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an1 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["мое_задание_2анализ"])
async def command_w2an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an2 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["мое_задание_3анализ"])
async def command_w3an(message: types.Message):
    await bot.send_message(message.from_user.id,
                           cur.execute('SELECT an3 FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[
                               0])


@dp.message_handler(commands=["задание_1планирование"])
async def command_w1org(message: types.Message):
    await bot.send_message(message.from_user.id, xx[0][0])


@dp.message_handler(commands=["задание_2планирование"])
async def command_w2org(message: types.Message):
    await bot.send_message(message.from_user.id, xx[0][1])


@dp.message_handler(commands=["задание_3планирование"])
async def command_w3org(message: types.Message):
    await bot.send_message(message.from_user.id, xx[0][2])


@dp.message_handler(commands=["задание_4планирование"])
async def command_w4org(message: types.Message):
    await bot.send_message(message.from_user.id, xx[0][3])


@dp.message_handler(commands=["задание_1управление"])
async def command_w1rul(message: types.Message):
    await bot.send_message(message.from_user.id, xx[1][0])
    print(xx[1][0])


@dp.message_handler(commands=["задание_2управление"])
async def command_w2rul(message: types.Message):
    await bot.send_message(message.from_user.id, xx[1][1])


@dp.message_handler(commands=["задание_3управление"])
async def command_w3rul(message: types.Message):
    await bot.send_message(message.from_user.id, xx[1][2])


@dp.message_handler(commands=["задание_4управление"])
async def command_w4rul(message: types.Message):
    await bot.send_message(message.from_user.id, xx[1][3])


@dp.message_handler(commands=["задание_1коммуникации"])
async def command_w1comm(message: types.Message):
    await bot.send_message(message.from_user.id, xx[2][0])


@dp.message_handler(commands=["задание_2коммуникации"])
async def command_w2comm(message: types.Message):
    await bot.send_message(message.from_user.id, xx[2][1])


@dp.message_handler(commands=["задание_3коммуникации"])
async def command_w3comm(message: types.Message):
    await bot.send_message(message.from_user.id, xx[2][2])


@dp.message_handler(commands=["задание_4коммуникации"])
async def command_w4comm(message: types.Message):
    await bot.send_message(message.from_user.id, xx[2][3])


@dp.message_handler(commands=["задание_1анализ"])
async def command_w1an(message: types.Message):
    await bot.send_message(message.from_user.id, xx[3][0])


@dp.message_handler(commands=["задание_2анализ"])
async def command_w2an(message: types.Message):
    await bot.send_message(message.from_user.id, xx[3][1])


@dp.message_handler(commands=["задание_3анализ"])
async def command_w3an(message: types.Message):
    await bot.send_message(message.from_user.id, xx[3][2])


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_tasks, commands=['tasks'])
    dp.register_message_handler(command_list, commands=['list'])
    dp.register_message_handler(command_profile, commands=['profile'])
    dp.register_message_handler(command_test, commands=['test'])
    dp.register_message_handler(command_configurations, commands=['config'])

    dp.register_message_handler(command_1org, commands=['1планирование'])
    dp.register_message_handler(command_2org, commands=['2планирование'])
    dp.register_message_handler(command_3org, commands=['3планирование'])
    dp.register_message_handler(command_4org, commands=['4планирование'])

    dp.register_message_handler(command_1rul, commands=['1управление'])
    dp.register_message_handler(command_2rul, commands=['2управление'])
    dp.register_message_handler(command_3rul, commands=['3управление'])
    dp.register_message_handler(command_4rul, commands=['4управление'])

    dp.register_message_handler(command_1comm, commands=['1коммуникации'])
    dp.register_message_handler(command_2comm, commands=['2коммуникации'])
    dp.register_message_handler(command_3comm, commands=['3коммуникации'])
    dp.register_message_handler(command_4comm, commands=['4коммуникации'])

    dp.register_message_handler(command_1an, commands=['1анализ'])
    dp.register_message_handler(command_2an, commands=['2анализ'])
    dp.register_message_handler(command_3an, commands=['3анализ'])

    dp.register_message_handler(command_w1org, commands=['мое_задание_1планирование'])
    dp.register_message_handler(command_w2org, commands=['мое_задание_2планирование'])
    dp.register_message_handler(command_w3org, commands=['мое_задание_3планирование'])
    dp.register_message_handler(command_w4org, commands=['мое_задание_4планирование'])

    dp.register_message_handler(command_w1rul, commands=['мое_задание_1управление'])
    dp.register_message_handler(command_w2rul, commands=['мое_задание_2управление'])
    dp.register_message_handler(command_w3rul, commands=['мое_задание_3управление'])
    dp.register_message_handler(command_w4rul, commands=['мое_задание_4управление'])

    dp.register_message_handler(command_w1comm, commands=['мое_задание_1коммуникации'])
    dp.register_message_handler(command_w2comm, commands=['мое_задание_2коммуникации'])
    dp.register_message_handler(command_w3comm, commands=['мое_задание_3коммуникации'])
    dp.register_message_handler(command_w4comm, commands=['мое_задание_4коммуникации'])

    dp.register_message_handler(command_w1an, commands=['мое_задание_1анализ'])
    dp.register_message_handler(command_w2an, commands=['мое_задание_2анализ'])
    dp.register_message_handler(command_w3an, commands=['мое_задание_3анализ'])

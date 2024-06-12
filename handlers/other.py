from aiogram import types, Dispatcher

from handlers import client, admin
from keyboards import *
from create_bot import bot, dp, base, cur
from data_base.tests import x
from admins_id import admin_id

async def text_messages(message: types.Message):
    id = message.from_user.id
    if int(cur.execute('SELECT passing_test FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == 1:
        cur.execute("UPDATE humans SET answer == ? WHERE id == ?", (message.text, id))
        base.commit()
        nn = cur.execute('SELECT test FROM humans WHERE id == ?', (int(id),)).fetchone()
        username = cur.execute("SELECT name FROM humans WHERE id == ?", (int(id),)).fetchone()
        print(str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]))
        if (str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '1') or (
                str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '2') or (
                str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '3') or (
                str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '4'):

            cur.execute("UPDATE humans SET test == ? WHERE id == ?", (int(nn[0]) + 1, id))
            base.commit()
            if str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '1':
                n = cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()
                print(int(n[0]))
                cur.execute("UPDATE humans SET technician == ? WHERE id == ?", (int(n[0]) + 1, id))
                base.commit()
            elif str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '2':
                n = cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()
                print(int(n[0]))
                cur.execute("UPDATE humans SET bio_chemical == ? WHERE id == ?", (int(n[0]) + 1, id))
                base.commit()
            elif str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '3':
                n = cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()
                print(int(n[0]))
                cur.execute("UPDATE humans SET social_economy == ? WHERE id == ?", (int(n[0]) + 1, id))
                base.commit()
            elif str(cur.execute('SELECT answer FROM humans WHERE id == ?', (int(id),)).fetchone()[0]) == '4':
                n = cur.execute('SELECT language FROM humans WHERE id == ?', (int(id),)).fetchone()
                print(int(n[0]))
                cur.execute("UPDATE humans SET language == ? WHERE id == ?", (int(n[0]) + 1, id))
                base.commit()

            await message.answer('\n'.join(x[nn[0]]))
        else:
            await message.answer("напиши номер ответа, который ты выбрал!")
        if nn[0] == len(x) - 1:
            await bot.send_message(message.from_user.id, f"твои результаты: \n"
                                                         f"технологическое направление - {cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()[0]} \n"
                                                         f"био-химическое направление - {cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()[0]} \n"
                                                         f"социально-экономическое направление - {cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()[0]} \n"
                                                         f"языковедение - {cur.execute('SELECT language FROM humans WHERE id == ?', (int(id),)).fetchone()[0]} \n")
            if cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()[0] == max(
                    cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT language FROM humans WHERE id == ?', (int(id),)).fetchone()[0]):
                cur.execute("UPDATE humans SET result == ? WHERE id == ?", ("технологическое направление", int(id)))
                base.commit()
                await bot.send_message(message.from_user.id,
                                       f'твой самый высокий результат - {"технологическое направление"} \n если что, тест можно перепройти')

            elif cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()[0] == max(
                    cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT language FROM humans WHERE id == ?', (int(id),)).fetchone()[0]):
                cur.execute("UPDATE humans SET result == ? WHERE id == ?", ("био-химическое направление", int(id)))
                base.commit()
                await bot.send_message(message.from_user.id,
                                       f'твой самый высокий результат - {"био-химическое направление"} \n если что, тест можно перепройти')

            elif cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()[0] == max(
                    cur.execute('SELECT technician FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT bio_chemical FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT social_economy FROM humans WHERE id == ?', (int(id),)).fetchone()[0],
                    cur.execute('SELECT language FROM humans WHERE id == ?', (int(id),)).fetchone()[0]):
                cur.execute("UPDATE humans SET result == ? WHERE id == ?",
                            ("социально-экономическое направление", int(id)))
                base.commit()
                await bot.send_message(message.from_user.id,
                                       f'твой самый высокий результат - {"социально-экономическое направление"} \n если что, тест можно перепройти')

            else:
                cur.execute("UPDATE humans SET result == ? WHERE id == ?", ("языковедение", int(id)))
                base.commit()
                await bot.send_message(message.from_user.id,
                                       f'твой самый высокий результат - {"языковедение"} \n если что, тест можно перепройти')

            cur.execute("UPDATE humans SET passing_test == ? WHERE id == ?", (0, int(id)))
            base.commit()

            client.b = []
    if int(cur.execute('SELECT config_choice FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0]) == 1:
        if message.text == 'да':
            if cur.execute('SELECT mastermind_message FROM humans WHERE id == ?', (int(message.from_user.id),)).fetchone()[0] == 1:
                cur.execute('UPDATE humans SET mastermind_message == ? WHERE id == ?', (0, int(message.from_user.id)))
                base.commit()
                await bot.send_message(message.from_user.id, 'вы больше не подписаны на рассылку', reply_markup=kb_client)
            else:
                cur.execute('UPDATE humans SET mastermind_message == ? WHERE id == ?', (1, int(message.from_user.id)))
                base.commit()
                await bot.send_message(message.from_user.id, 'вы подписались на рассылку', reply_markup=kb_client)
        elif message.text == 'отмена':
            await bot.send_message(message.from_user.id, 'отменено', reply_markup=kb_client)
        cur.execute('UPDATE humans SET config_choice == ? WHERE id == ?', (0, int(message.from_user.id)))

    if message.text.lower() == 'назад':
        await bot.send_message(message.from_user.id, 'назад', reply_markup=kb_client)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(text_messages)

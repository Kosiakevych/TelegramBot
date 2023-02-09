from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.executor import start_polling
from days import what_month, choice_day
from callback_button import *
from config import dp
from google_calendar import total, get_calendar_data, delete_event, my_entry_list
from translate import translate_app as trl

client_description = []  # Which service
client_date = []  # Which date
client_name = []  # Name and phone of user
client_time = []  # Which time
count_for_sql_delete = []  # for delete entry | which entry user want to delete
language = [False]  # False -> language russian | True language ukraine
client_id = []  # verification of user | did user send his contact | if not -> bot will not work


@dp.message_handler(Command('help'))
async def command_help(message: Message):
    await message.answer(f'{trl(language[0], "Нмр")}\n👉 <b>+380950988023</b>\n👉 <b>+4915158482594</b>',
                         parse_mode='html')
    await message.answer_contact('380950988023', first_name=f"{trl(language[0], 'Мария')}", last_name='Гнатюк')


@dp.message_handler(Command('start'))  # start bot
async def start(message: Message):
    client_id.append(message["from"]["id"])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(text="📱 Отправить номер телефона👇", request_contact=True))

    await message.answer("📲 Отправь свой контакт✅", reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.CONTACT)  # get data from user
async def get_user_data(message: Message):
    if message['contact']["user_id"] != client_id[0]:  # if user try to send not his contact
        await message.answer('Id Пользователей не совпадает')
    else:  # if user send his contact
        client_name.clear()  # if user clicked to back button
        client_name.append(message['contact']['first_name'])  # append to list name | for Google calendar API
        client_name.append(message['contact']['phone_number'])  # append to list phone number | for Google calendar API
        remove_button = types.ReplyKeyboardRemove()  # for remove button "send phone"
        await message.answer('✅', reply_markup=remove_button)  # remove keyboard markup
        await message.answer(text='-----------------------------\n\n'
                                  '● Привет, Здесь вы можете записаться с Пн - Пт\n\n '  # title
                                  '● Если возникли проблемы\nто нажмите сюда 👉 /help\n\n-----------------------------')
        await message.answer(text='<b>⠀       💛 Выберите Действие👇</b>', parse_mode='html',
                             reply_markup=first_choice(language[0]))


@dp.callback_query_handler(text_contains='language:ua')  # if user want to change language to ukrainian
async def change_language(call: CallbackQuery):
    language[0] = True
    await call.message.edit_text(text='<b>⠀                 💛 Оберіть Дію👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(first_choice(language[0]))


@dp.callback_query_handler(text_contains='language:ru')  # if user want to change language to russian
async def change_language(call: CallbackQuery):
    language[0] = False
    await call.message.edit_text(text='<b>⠀       💛 Выберите Действие👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(first_choice(language[0]))


@dp.callback_query_handler(text_contains='first:back')  # for button 'back'
async def back_start(call: CallbackQuery):
    text = '          💛 Оберіть Дію' if language[0] else '💛 Выберите Действие'  # depends on language which user chose
    await call.message.edit_text(text=f'<b>⠀       {text}👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(first_choice(language[0]))


@dp.callback_query_handler(text_contains='my_entry')  # user entry | my_entry:my | my_entry:delete
async def entry(call: CallbackQuery):
    entry_list = my_entry_list(client_name)  # get text(array) of user entry
    text = trl(language[0], 'Мои записи', entry_list[0])  # translate to ukrainian if user changed language
    if len(text) < 23:  # If user has not any entry
        text = f"<b>🗓️ {trl(language[0], 'Уваснет')} 📂</b>"
    await call.message.edit_text(text=text, parse_mode='html')

    if call["data"] == "my_entry:my":  # if user chose my_entry:my
        await call.message.edit_reply_markup(reply_markup=back_to_entry(language[0]))
    else:  # if user chose my_entry:delete
        await call.message.edit_reply_markup(reply_markup=delete_entry_button(entry_list[1], language[0]))


@dp.callback_query_handler(text_contains='try_delete')  # are you sure you want to delete entry?
async def try_delete(call: CallbackQuery):
    name = ', '.join(client_name)  # ['Alex', '123'] -> 'Alex, 123'
    count_for_sql_delete.clear()  # if user clicked to back button
    count_for_sql_delete.append(int(call['data'][-1]))  # 'delete:0' -> '0'
    count = count_for_sql_delete[0]  # [0] -> 0
    data_time = get_calendar_data(name)[2][count]  # 2022-12-12 14:00
    await call.message.edit_text(text=f'📕 {trl(language[0], "Уд?")}'
                                      f'\n<b>Дата: {data_time[1]}'  # 2022-12-12
                                      f' {trl(language[0], "Время")}:'
                                      f'{data_time[2]}</b>',  # 14:00
                                 parse_mode='html')
    await call.message.edit_reply_markup(delete_or_not(language[0]))  # yes | no


@dp.callback_query_handler(text_contains='delete')  # my entry and delete entry
async def delete(call: CallbackQuery):
    count = count_for_sql_delete[0]  # [0] -> 0
    name = ', '.join(client_name)  # ['Alex', '123'] -> 'Alex, 123'
    event_id = get_calendar_data(name)[3][count]  # get_calendar_data[eventID][0] -> '9vfge4sqhdi1ef32kfgjh2fj2s'
    delete_event(event_id)  # send request to delete_event
    await call.answer(text='Запись удалена')  # show text

    await call.message.edit_text(text='<b>⠀       💛 Выберите Действие👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(first_choice(language[0]))


@dp.callback_query_handler(text_contains='entry:make')  # choice option
async def work_with_entry(call: CallbackQuery):
    await call.message.edit_text(text=f'<b>🎀 {trl(language[0], "ВОпцию")}👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=option_choice(language[0]))


@dp.callback_query_handler(text_contains='depilation')  # choice depilation
async def choice_of_depilation(call: CallbackQuery):
    client_description.clear()  # if user clicked to back button
    client_description.append('Депиляция ')  # add 'service' to list for Google calendar API

    await call.message.edit_text(text=f'<b>💚 {trl(language[0], "ВЗону")}👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=service_of_first_choice(language[0]))


@dp.callback_query_handler(text_contains='service')  # choice month
async def choice_of_month(call: CallbackQuery):
    if not call['data'] == 'service:back':  # in case if you click on back button then replace service -> back
        client_description.pop(-1) if len(client_description) == 2 else None  # if user clicked to back button
    # if user clicked to back button and after depilation chose service:eyelashes
    client_description.pop(0) if call['data'] == 'service:eyelashes' and len(client_description) != 0 else None
    # add 'service' to list for Google calendar API
    match call['data']:  # translate for Google calendar API and for entry:my
        case 'service:eyelashes':
            client_description.append('Реснички')
        case 'service:bikini':
            client_description.append('Бикини 30 €, 20 мин')
        case 'service:legs':
            client_description.append('Ноги 45 €, 40 мин')
        case 'service:arm':
            client_description.append('Руки 20 €, 15 мин')
        case 'service:face':
            client_description.append('Лицо 10 €, 10 мин')

    await call.message.edit_text(text=f'<b>⠀             🗓️ {trl(language[0], "ВМесяц")}👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=choice_month(language[0]))


@dp.callback_query_handler(text_contains='month')  # choice day
async def choice_of_day(call: CallbackQuery):
    what_month_number = what_month(1 if call['data'] == 'month:next_month' else 0)  # send request to days.py

    client_date.clear()  # if user clicked to back button
    client_date.append(what_month_number[1])  # append to list year '2023'| for Google calendar API and SQL
    client_date.append(what_month_number[0])  # append to list month '01' | for Google calendar API and SQL

    await call.message.edit_text(text=f'<b>⠀     📌 {trl(language[0], "ВДень")}👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=choice_day)


@dp.callback_query_handler(text_contains='day')  # choice time
async def choice_of_time(call: CallbackQuery):
    # append to list day | 'day:25' -> '25' | 'day:3' -> '03' | for google calendar API and SQL
    if call['data'] != 'day:back_to_time':  # do not append call['data'] if user chose button back
        client_date.append(call['data'][4:] if len(call['data'][4:]) == 2 else f"0{call['data'][4:]}")
    time_button = show_time(client_date, language[0])  # create time button

    await call.message.edit_text(text=f'<b>📍 {trl(language[0], "Ввыбрали")} <U>{client_date[2]}</U>'
                                      f' Число\n⏳ {trl(language[0], "ВВремя")}👇</b>', parse_mode='html')
    if len(time_button["inline_keyboard"]) == 1:  # if all time have been already taken
        await call.message.edit_text(f"<b>⠀     🔴 {trl(language[0], 'Занято')} 🔴</b>", parse_mode="html")
    await call.message.edit_reply_markup(reply_markup=time_button)


@dp.callback_query_handler(text_contains='time')  # send contact
async def get_contact(call: CallbackQuery):
    client_time.clear()  # if user clicked to back button
    client_time.append(call['data'][5:])  # append to list '16' | 'time:16' -> 16 | for google calendar API and SQL

    await call.message.edit_text(f'{trl(language[0], "Взаписаться")}\n<b>Дата: {"-".join(client_date)} | '
                                 f'{"Час" if language[0] else "Время"}: {client_time[0]}:00</b>', parse_mode='html')
    await call.message.edit_reply_markup(confirm_date(language[0]))


@dp.callback_query_handler(text_contains='confirm:yes')  # before send to Google cal and SQL
async def confirm_entry(call: CallbackQuery):
    total(client_name, client_description, client_date, client_time)  # send request for google calendar API

    await call.message.edit_text(text=f'<b>✅ {trl(language[0], "Отлично")}🤩</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=back_to_entry(language[0]))


@dp.message_handler()  # for message which bot did not understand
async def catch_random_message(message: Message):
    await message.answer(f'<b>{trl(language[0], "Непоняла")}</b>', parse_mode='html')


start_polling(dp)

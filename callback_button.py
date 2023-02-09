from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from days import current_date
from google_calendar import check_free_space as cfs
from translate import translate_button as trl


def first_choice(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'✏️ {trl(language, "Зап")}', callback_data='entry:make')
            ],
            [
                InlineKeyboardButton(text=f'📂 {trl(language, "Мзап")}', callback_data="my_entry:my"),
                InlineKeyboardButton(text=f'🗑️ {trl(language, "Узап")}', callback_data="my_entry:delete"),
            ],
            [
                InlineKeyboardButton(text=f'{trl(language, "Язык")}',
                                     callback_data=f'language:{"ru" if language else "ua"}')
            ]
        ]
    )


def option_choice(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'😽 {trl(language, "Ресн")}', callback_data='service:eyelashes'),
            ],
            [
                InlineKeyboardButton(text=f'❤️ {trl(language, "Деп")}', callback_data="depilation"),
            ],
            [
                InlineKeyboardButton(text=f'⬅️ {trl(language, "НДей")}', callback_data="first:back"),
            ],
        ]
    )


def service_of_first_choice(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'👙 {trl(language, "Бикини")}', callback_data='service:bikini')
            ],
            [
                InlineKeyboardButton(text=f'🦵 {trl(language, "Ноги")}', callback_data="service:legs"),
            ],
            [
                InlineKeyboardButton(text=f'💪 {trl(language, "Руки")}', callback_data='service:arm')
            ],
            [
                InlineKeyboardButton(text=f'😌 {trl(language, "Лицо")}', callback_data="service:face"),
            ],
            [
                InlineKeyboardButton(text=f'⬅️ {trl(language, "НОпц")}', callback_data="entry:make"),
            ],
        ]
    )


def choice_month(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'📅 {trl(language, "Этотм")} 📅', callback_data='month:this_month'),
                InlineKeyboardButton(text=f'➡️ {trl(language, "Следм")} ➡️', callback_data="month:next_month"),
            ],
            [
                InlineKeyboardButton(text=f'⬅️ {trl(language, "НОпц")}', callback_data="entry:make"),
            ],
        ]
    )


def back_to_entry(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'⬅️ {trl(language, "НДей")}', callback_data="first:back"),
            ]
        ]
    )


def delete_or_not(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'✅ {trl(language, "Удал")}', callback_data="delete"),
            ],
            [
                InlineKeyboardButton(text=f'⬅️ {trl(language, "Нвыбору")}', callback_data="my_entry:delete"),
            ]
        ]
    )


def confirm_date(language: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'✅ {"Так" if language else "Да"}', callback_data="confirm:yes"),
                InlineKeyboardButton(text=f'❌ {"Ні" if language else "Нет"}', callback_data="day:back_to_time"),
            ],
        ]
    )


def show_time(client_date: list, language: bool):
    choice_time = InlineKeyboardMarkup(row_width=3)
    # free_space = get_empty_space(client_date)  # get info from SQL, how many cell in day we have
    date = '-'.join(client_date)
    time_list = [10, 12, 14, 16, 18]  # which time client can make entry
    for time_but in time_list:
        # time_but = time_but + 14  # 14 || 15 || 16
        choice_time.insert(InlineKeyboardButton(
            text=f'{time_but}:00', callback_data=f'time:{time_but}'
        )) if cfs(date + f"T{time_but}") else None
    choice_time.row(InlineKeyboardButton(text=f'⬅️{trl(language, "Ндня")}', callback_data="service:back"))

    return choice_time  # return Markup


def delete_entry_button(entry_data: list, language: bool):
    delete_entry_markup = InlineKeyboardMarkup(row_width=1)  # add markup
    count = 0
    for i in entry_data:  # ['Удалить запись: ', date, time]
        check_data = int(''.join(i[1].split('-')))  # '2022-12-12' -> 20221212
        current = int(current_date())  # current year, month, day -> 20221212
        if check_data >= current:  # if entry not in the past, user can delete it
            text = ' '.join(i)
            text = text.replace('Удалить запись', "Видалити запис") if language else text
            text = text.replace('Время', "Час") if language else text
            delete_entry_markup.insert(InlineKeyboardButton(text=text, callback_data=f"try_delete:{count}"))
        count += 1
    delete_entry_markup.row(InlineKeyboardButton(text=f'⬅️ {trl(language, "НДей")}', callback_data="first:back"))
    return delete_entry_markup

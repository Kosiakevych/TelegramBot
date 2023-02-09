# Translate from Russian to Ukrainian

# Translate in app.py
# Help
def translate_app(language: bool, which_text: str, *args) -> str:
    match which_text:
        case 'Нмр': return 'Номера телефона Марії' if language else "Номера телефона Марии"
        case 'Мария': return 'Марія' if language else 'Мария'
        case 'Мои записи':
            text = args[0].replace('Время', 'Час') if language else args[0]
            rus_list = ['Услуга', 'мин', 'Реснички', 'Депиляция', 'Бикини', 'Лицо', "Запись создана"]  # rus word
            ua_list = ['Послуга', 'хв', 'Вії', 'Депіляція', 'Бікіні', 'Обличчя', "Запис створено"]  # ua word
            for i in range(len(rus_list)):  # translate rus -> ua if user chose ukrainian
                text = text.replace(rus_list[i], ua_list[i]) if language else text
            return text
        case 'ВОпцию': return "Оберіть Опцію" if language else 'Выберите Опцию'
        case 'ВЗону': return "Оберіть Зону" if language else 'Выберите Зону'
        case 'ВМесяц': return "Оберіть Місяць" if language else 'Выберите Месяц'
        case 'ВДень': return "Оберіть День" if language else 'Выберите День'
        case 'Ввыбрали': return "Ви обрали" if language else 'Вы выбрали'
        case 'ВВремя': return "Оберіть час" if language else 'Выберите Время'
        case 'Взаписаться':
            return "Ви впевнені, що хочете записатися на" if language else 'Вы уверены что хотите записаться на'
        case "Отлично": return 'Добре, я вас записала' if language else 'Отлично, я вас записала'
        case "Непоняла": return 'Я вас не зрозуміла🧐\n\n💜 Будь ласка, користуйтесь кнопками😌' \
            if language else 'Я вас не поняла🧐\n\n💜 Пожалуйста, пользуйтесь кнопками😌'
        case 'Уд?': return "Видалити цей запис?" if language else "Удалить эту запись?"
        case 'Время': return "Час" if language else "Время"
        case 'Занято': return "На сьогодні все зайняте" if language else "На сегодня все занято"
        case 'Уваснет': return "У вас немає записів" if language else "У вас нет записей"


def translate_button(language: bool, which_text: str) -> str:
    match which_text:
        # option_choice
        case "Ресн": return "Вії" if language else "Реснички"
        case "Деп": return "Депіляція" if language else "Депиляция"
        case "НДей": return "Назад до вибору Дії" if language else "Назад к выбору Действия"
        # service_of_first_choice
        case "Бикини": return "Бікіні 30 євро, 20 хв" if language else "Бикини 30 евро, 20 мин"
        case "Ноги": return "Ноги 45 євро, 40 хв" if language else "Ноги 45 евро, 40 мин"
        case "Руки": return "Руки 20 євро, 15 хв" if language else "Руки 20 евро, 15 мин"
        case "Лицо": return "Обличчя 10 євро, 10 хв" if language else "Лицо 10 евро, 10 мин"
        case "НОпц": return "Назад до вибору Опції" if language else "Назад к выбору Опциии"
        # choice_month
        case "Этотм": return "Цей місяць" if language else "Этот месяц"
        case "Следм": return "Наступний місяць" if language else "Следующий месяц"
        # show_time
        case "Ндня": return "Назад до вибору дня" if language else "Назад к выбору дня"
        # delete_or_not
        case "Удал": return "Видалити" if language else "Удалить"
        case "Нвыбору": return "Назад до вибору" if language else "Назад к выбору"
        # first_choice
        case "Зап": return "Записатись" if language else "Записаться"
        case "Мзап": return "Мої записи" if language else "Мои записи"
        case "Узап": return "Видалити запис" if language else "Удалить запись"
        case "Язык": return "🏳️ Русский" if language else "🇺🇦 Українська"




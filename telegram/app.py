import json
import requests
import telebot
from telebot import types
from config import Config
from keyboards import keyboardMenuEmployer, keyboardMenuCondidate, keyboardStart
from loguru import logger

config = Config()
bot = telebot.TeleBot(config.BOT_TOKEN)
logger.info(' [X] START TELEGRAM BOT')

LEVEL_EMPLOYER = {
    1: {"method": "company", "tip": "В какой компании вы работаете:", "status": "reg"},
    2: {"method": "category", "tip": "Укажите профиль деятельности:", "status": "reg"},
    3: {"method": "address", "tip": "Укажите адрес:", "status": "reg"},
    4: {"method": "fio", "tip": "ФИО контактного лица:", "status": "reg"},
    5: {"method": "phone", "tip": "Контактный номер телефона:", "status": "reg"},
    6: {"method": "email", "tip": "Почта:", "status": "reg"},
    7: {"method": "url", "tip": "URL:", "status": "reg"},
    8: {"method": "", "tip": "", "status": "done"},
}

LEVEL_CANDIDAT = {
    1: {"method": "name", "tip": "Ваше имя:", "status": "reg"},
    2: {"method": "secondname", "tip": "Фамилия:", "status": "reg"},
    3: {"method": "age", "tip": "Возраст:", "status": "reg"},
    4: {"method": "address", "tip": "Адрес:", "status": "reg"},
    5: {"method": "phone", "tip": "Контактный номер телефона:", "status": "reg"},
    6: {"method": "email", "tip": "Почта:", "status": "reg"},
    7: {"method": "url", "tip": "Cсылка на соц. сети:", "status": "reg"},
    8: {"method": "", "tip": "", "status": "done"},
}

def AK47(user, LEVEL, message):
    for i, v in LEVEL.items():
        if user['level'] == v['method']:
            next_level = LEVEL[i+1]
            logger.info(f"{user['chat_id']} -> method {next_level['method']}")
            config.db.update_one(user, {"$set": {"status": v['status'], "level": next_level['method'], v['method']: message.text}})
            if next_level['tip']:
                bot.send_message(message.chat.id, next_level['tip'])
            if next_level['status'] == "done":
                return True
    return False


@bot.message_handler(commands=['clear'])
def clear(message):
    user = config.db.find({"chat_id": message.chat.id})[0]
    config.db.update_one(user, {"$set": {"status": "reg", "level": "", "type": ""}})


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        logger.info('Get user from db')
        user = config.db.find({"chat_id": message.chat.id})[0]
    except:
        logger.info('First registration user in db')
        config.db.insert_one({"chat_id": message.chat.id})
        user = config.db.find({"chat_id": message.chat.id})[0]

    if 'type' not in user or user['type'] == None or user['type'] == "":
        logger.info("User doesn't has type")
        bot.send_message(message.chat.id, 'Привет, я бот созданный для ....', reply_markup=keyboardStart())
        config.db.update_one(user, {"$set": {"status": "reg"}})
    else:
        logger.info(f"User: {user}")
        if user['type'] == 'employer':
            if user['status'] == 'reg':
                logger.info("Continue registration employer")
                if user['level'] == "":
                    config.db.update_one(user, {"$set": {"level": LEVEL_EMPLOYER[1]['method']}})
                    bot.send_message(message.chat.id, LEVEL_EMPLOYER[1]['tip'])
                else:
                    for i, v in LEVEL_EMPLOYER.items():
                        if user['level'] == v['method']:
                            bot.send_message(message.chat.id, v['tip'])
                            break
            else:
                logger.info("Get menu emploer")
                bot.send_message(message.chat.id, 'Главное меню работодателя!', reply_markup=keyboardMenuEmployer())

        elif user['type'] == 'condidate':
            logger.info("Get menu condidate")
            bot.send_message(message.chat.id, 'Главное меню соискателя!', reply_markup=keyboardMenuCondidate())


@bot.callback_query_handler(func=lambda call: config.db.find({"chat_id": call.message.chat.id})[0]['status'] == 'reg')
def startRegUser(call):
    user = config.db.find({"chat_id": call.message.chat.id})[0]
    if call.message:
        logger.info(f"Callback: {call.data}")
        if call.data == "employer":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=LEVEL_EMPLOYER[1]['tip'])
            config.db.update_one(user, {"$set": {"level": LEVEL_EMPLOYER[1]['method'], "type": call.data}})
        if call.data == "condidate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=LEVEL_CANDIDAT[1]['tip'])
            config.db.update_one(user, {"$set": {"level": LEVEL_CANDIDAT[1]['method'], "type": call.data}})


@bot.message_handler(content_types=["text"],
                     func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'employer'
                                          and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegEmployer(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]
    if AK47(employer, LEVEL_EMPLOYER, message):
        data = {
            'username': message.from_user.username,
            'email': employer['email'],
            'company': employer['company'],
            'category': employer['category'],
            'address': employer['address'],
            'fio': employer['fio'],
            'phone': employer['phone'],
            'url': employer['url'],

        }
        requests.post(url=config.HOST + 'create/employer/', data=data)

        bot.send_message(message.chat.id,
                         'Спасибо за регистрацию. Теперь вы можете создавать вакансии',
                         reply_markup=keyboardMenuEmployer())



@bot.message_handler(content_types=["text"],
                     func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'condidate'
                                          and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegCandidat(message):
    candidat = config.db.find({"chat_id": message.chat.id})[0]
    if AK47(candidat, LEVEL_CANDIDAT, message):
        data = {
            'username': message.from_user.username,
            'email': candidat['email'],
            'name': candidat['name'],
            'secondname': candidat['secondname'],
            'age': candidat['age'],
            'address': candidat['address'],
            'fio': candidat['fio'],
            'phone': candidat['phone'],
            'url': candidat['url'],

        }
        requests.post(url=config.HOST + 'create/condidate/', data=data)
        config.db.update_one(candidat, {"$set": {"status": "done"}})

        markup = keyboardMenuCondidate()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать резюму',
                         reply_markup=markup)


if __name__ == '__main__':
    bot.polling()

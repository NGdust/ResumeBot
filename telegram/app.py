import json
import requests
import telebot
from telebot import types
from config import Config
from keyboards import keyboardMenuEmployer, keyboardMenuCondidate, keyboardStart


config = Config()
bot = telebot.TeleBot(config.BOT_TOKEN)
print(' [X] START TELEGRAM BOT')


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        user = config.db.find({"chat_id": message.chat.id})[0]
    except:
        config.db.insert_one({"chat_id": message.chat.id, "username": message.from_user.username})
        user = config.db.find({"chat_id": message.chat.id})[0]

    if 'type' not in user or user['type'] == None:
        bot.send_message(message.chat.id, 'Привет, я бот созданный для ....', reply_markup=keyboardStart())
        config.db.update_one(user, {"$set": {"status": "reg", "type": ''}})
    else:
        if user['type'] == 'employer':
            bot.send_message(message.chat.id, 'Главное меню работодателя!', reply_markup=keyboardMenuEmployer())
        elif user['type'] == 'condidate':
            bot.send_message(message.chat.id, 'Главное меню соискателя!', reply_markup=keyboardMenuCondidate())


@bot.message_handler(commands=['reset'])
def resetUser(message):
    try:
        user = config.db.find({"chat_id": message.chat.id})[0]
    except:
        bot.send_message(message.chat.id, 'Вы еще не зарегистрировались', reply_markup=keyboardStart())



@bot.callback_query_handler(func=lambda call: config.db.find({"chat_id": call.message.chat.id})[0]['status'] == 'reg')
def startRegUser(call):
    user = config.db.find({"chat_id": call.message.chat.id})[0]
    if call.message:
        if call.data == "employer":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="В какой компании вы работаете:")
            config.db.update_one(user, {"$set": {"level": "getCompany", "type": call.data}})
        if call.data == "condidate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ваше имя:")
            config.db.update_one(user, {"$set": {"level": "getName", "type": call.data}})

        if call.data == "create_vacansy":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="На какую должность:")
            config.db.update_one(user, {"$set": {"level": "getPosition"}})

def sendCreateEmployer(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]
    data = {
        'username': employer['username'],
        'email': employer['email'],
        'company': employer['company'],
        'category': employer['category'],
        'address': employer['address'],
        'fio': employer['fio'],
        'phone': employer['phone'],
        'url': employer['url'],
        'chat_id': employer['chat_id'],

    }
    requests.post(url=config.HOST + 'create/employer/', data=data)

@bot.message_handler(content_types=["text"], func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'employer'
                                                                  and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegEmployer(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]

    if employer['level'] == 'getCompany':
        config.db.update_one(employer, {"$set": {"level": "getCategory", "company": message.text}})
        bot.send_message(message.chat.id, 'Укажите профиль деятельности:')
    elif employer['level'] == 'getCategory':
        config.db.update_one(employer, {"$set": {"level": "getAddress", "category": message.text}})
        bot.send_message(message.chat.id, 'Укажите адрес:')
    elif employer['level'] == 'getAddress':
        config.db.update_one(employer, {"$set": {"level": "getFio", "address": message.text}})
        bot.send_message(message.chat.id, 'ФИО контактного лица:')
    elif employer['level'] == 'getFio':
        config.db.update_one(employer, {"$set": {"level": "getPhone", "fio": message.text}})
        bot.send_message(message.chat.id, 'Контактный номер телефона:')
    elif employer['level'] == 'getPhone':
        config.db.update_one(employer, {"$set": {"level": "getEmail", "phone": message.text}})
        bot.send_message(message.chat.id, 'Почта:')
    elif employer['level'] == 'getEmail':
        config.db.update_one(employer, {"$set": {"level": "getUrl", "email": message.text}})
        bot.send_message(message.chat.id, 'URL:')
    elif employer['level'] == 'getUrl':
        config.db.update_one(employer, {"$set": {"level": "", "url": message.text}})

        # Отправка на сервер
        sendCreateEmployer(message)
        config.db.update_one(employer, {"$set": {"status": "done"}})

        markup = keyboardMenuEmployer()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать вакансии', reply_markup=markup)


def sendCreateCandidate(message):
    candidat = config.db.find({"chat_id": message.chat.id})[0]
    data = {
        'username': candidat['username'],
        'email': candidat['email'],
        'name': candidat['name'],
        'secondname': candidat['secondname'],
        'age': candidat['age'],
        'address': candidat['address'],
        'fio': candidat['fio'],
        'phone': candidat['phone'],
        'url': candidat['url'],
        'chat_id': candidat['chat_id'],

    }
    requests.post(url=config.HOST + 'create/condidate/', data=data)

@bot.message_handler(content_types=["text"], func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'condidate'
                                                                  and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegCandidat(message):
    candidat = config.db.find({"chat_id": message.chat.id})[0]

    if candidat['level'] == 'getName':
        config.db.update_one(candidat, {"$set": {"level": "getSecondName", "name": message.text}})
        bot.send_message(message.chat.id, 'Фамилия:')
    if candidat['level'] == 'getSecondName':
        config.db.update_one(candidat, {"$set": {"level": "getAge", "secondname": message.text}})
        bot.send_message(message.chat.id, 'Возраст:')
    if candidat['level'] == 'getAge':
        config.db.update_one(candidat, {"$set": {"level": "getAddress", "age": message.text}})
        bot.send_message(message.chat.id, 'Адресс:')
    if candidat['level'] == 'getAddress':
        config.db.update_one(candidat, {"$set": {"level": "getEmail", "address": message.text}})
        bot.send_message(message.chat.id, 'Email:')
    if candidat['level'] == 'getEmail':
        config.db.update_one(candidat, {"$set": {"level": "getPhone", "email": message.text}})
        bot.send_message(message.chat.id, 'Телефон:')
    if candidat['level'] == 'getPhone':
        config.db.update_one(candidat, {"$set": {"level": "getUrl", "phone": message.text}})
        bot.send_message(message.chat.id, 'Cсылка на соц. сети:')
    elif candidat['level'] == 'getUrl':
        config.db.update_one(candidat, {"$set": {"level": "", "url": message.text}})

        # Отправка на сервер
        sendCreateCandidate(message)
        config.db.update_one(candidat, {"$set": {"status": "done"}})

        markup = keyboardMenuCondidate()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать резюму', reply_markup=markup)


@bot.message_handler(content_types=["text"], func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'employer'
                                                                  and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'done')
def pollCreateVacansy(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]

    if employer['level'] == 'getPosition':
        config.db.update_one(employer, {"$set": {"level": "getAgg", "a": message.text}})
        bot.send_message(message.chat.id, 'Укажите профиль деятельности:')
    elif employer['level'] == 'getCategory':
        config.db.update_one(employer, {"$set": {"level": "getAddress", "category": message.text}})
        bot.send_message(message.chat.id, 'Укажите адрес:')
    elif employer['level'] == 'getAddress':
        config.db.update_one(employer, {"$set": {"level": "getFio", "address": message.text}})
        bot.send_message(message.chat.id, 'ФИО контактного лица:')
    elif employer['level'] == 'getFio':
        config.db.update_one(employer, {"$set": {"level": "getPhone", "fio": message.text}})
        bot.send_message(message.chat.id, 'Контактный номер телефона:')
    elif employer['level'] == 'getPhone':
        config.db.update_one(employer, {"$set": {"level": "getEmail", "phone": message.text}})
        bot.send_message(message.chat.id, 'Почта:')
    elif employer['level'] == 'getEmail':
        config.db.update_one(employer, {"$set": {"level": "getUrl", "email": message.text}})
        bot.send_message(message.chat.id, 'URL:')
    elif employer['level'] == 'getUrl':
        config.db.update_one(employer, {"$set": {"level": "", "url": message.text}})

        # Отправка на сервер
        data = {
            'username': employer['username'],
            'email': employer['email'],
            'company': employer['company'],
            'category': employer['category'],
            'address': employer['address'],
            'fio': employer['fio'],
            'phone': employer['phone'],
            'url': employer['url'],

        }
        requests.post(url=config.HOST + 'create/employer/', data=data)
        config.db.update_one(employer, {"$set": {"status": "done"}})

        markup = keyboardMenuEmployer()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать вакансии', reply_markup=markup)

if __name__ == '__main__':
    bot.polling()
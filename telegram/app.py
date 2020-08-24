import json
import time

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


@bot.message_handler(commands=['menu'])
def start_message(message):
    try:
        user = config.db.find({"chat_id": message.chat.id})[0]
        if user['type'] == 'employer':
            bot.send_message(message.chat.id, 'Главное меню работодателя!', reply_markup=keyboardMenuEmployer())
        elif user['type'] == 'condidate':
            bot.send_message(message.chat.id, 'Главное меню соискателя!', reply_markup=keyboardMenuCondidate())
    except:
        bot.send_message(message.chat.id, 'Вы еще не зарегестрировались', reply_markup=keyboardStart())



@bot.message_handler(commands=['delete'])
def resetUser(message):
    try:
        user = config.db.find({"chat_id": message.chat.id})[0]
        config.db.delete_one(user)
        data = {
            "username": user['username'],
        }
        requests.post(config.HOST + config.USER_API + 'delete/', data=data)
        bot.send_message(message.chat.id, 'Ваша учетная запись удалена')
    except:
        bot.send_message(message.chat.id, 'Вы еще не зарегистрировались', reply_markup=keyboardStart())


@bot.callback_query_handler(func=lambda call: True)
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
        if call.data == "create_resume":
            data = {
                "username": user['username'],
            }
            responce = requests.post(config.HOST + config.DATA_API + 'resumes/', data=data)
            limitResume = 3
            if len(json.loads(responce.text)) < limitResume:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Укажите название компании в которой вы работали: ")
                config.db.update_one(user, {"$set": {"level": "getCompany"}})
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Нельзя создавать больше 3 резюме")

        if call.data == "vacansies":
            data = {
                "username": user['username'],
            }
            responce = requests.post(config.HOST + config.DATA_API + 'vacansies/', data=data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Ваши вакансии:")
            for item in json.loads(responce.text):
                text = f"Должность: {item['position']}\n" \
                       f"Опыт: {item['experience']}\n" \
                       f"Описание: {item['description']}\n" \
                       f"Зарплата: {item['salary']}"
                bot.send_message(call.message.chat.id, text=text)
        if call.data == "resumes":
            data = {
                "username": user['username'],
            }
            responce = requests.post(config.HOST + config.DATA_API + 'resumes/', data=data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Ваши резюме: ")
            resumes = json.loads(responce.text)
            for item in resumes:
                text = f"Компания: {item['company']}\n" \
                       f"Должность: {item['position']}\n" \
                       f"Опыт: {item['experience']}\n" \
                       f"Причина увольнения: {item['reason']}\n" \
                       f"Результаты/достяжения: {item['results']}"
                bot.send_message(call.message.chat.id, text=text)













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
    requests.post(url=config.HOST + config.USER_API + 'create/employer/', data=data)
    config.db.update_one(employer, {"$set": {"status": "done"}})


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
        'phone': candidat['phone'],
        'url': candidat['url'],
        'chat_id': candidat['chat_id'],

    }
    requests.post(url=config.HOST + config.USER_API + 'create/condidate/', data=data)
    config.db.update_one(candidat, {"$set": {"status": "done"}})

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


        markup = keyboardMenuCondidate()
        bot.send_message(message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать резюму', reply_markup=markup)


def sendCreateVacansy(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]
    data = {
        'username': employer['username'],
        'position': employer['position'],
        'experience': employer['experience'],
        'age': employer['age'],
        'salary': employer['salary'],
        'description': employer['description'],

    }
    requests.post(url=config.HOST + config.DATA_API + 'create/vacansy/', data=data)
    config.db.update_one(employer, {"$set": {"status": "done"}})


@bot.message_handler(content_types=["text"], func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'employer'
                                                                  and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'done')
def pollCreateVacansy(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]

    if employer['level'] == 'getPosition':
        config.db.update_one(employer, {"$set": {"level": "getExperience", "position": message.text}})
        bot.send_message(message.chat.id, 'Укажите опыт соискателя:')
    elif employer['level'] == 'getExperience':
        config.db.update_one(employer, {"$set": {"level": "getAge", "experience": message.text}})
        bot.send_message(message.chat.id, 'Укажите возраст соискателя:')
    elif employer['level'] == 'getAge':
        config.db.update_one(employer, {"$set": {"level": "getSalary", "age": message.text}})
        bot.send_message(message.chat.id, 'Сколько готовы платить будущему сотруднику:')
    elif employer['level'] == 'getSalary':
        config.db.update_one(employer, {"$set": {"level": "getDescription", "salary": message.text}})
        bot.send_message(message.chat.id, 'Укажите типовые задачи, которые должен будет выполнять Ваш сотрудник (в одном сообщении):')
    elif employer['level'] == 'getDescription':
        config.db.update_one(employer, {"$set": {"level": "", "description": message.text}})

        sendCreateVacansy(message)

        markup = keyboardMenuEmployer()
        bot.send_message(message.chat.id, 'Вы создали свою вакансию...', reply_markup=markup)


def sendCreateResume(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]
    data = {
        'username': employer['username'],
        'company': employer['company'],
        'position': employer['position'],
        'experience': employer['experience'],
        'results': employer['results'],
        'reason': employer['reason'],

    }
    requests.post(url=config.HOST + config.DATA_API + 'create/resume/', data=data)
    config.db.update_one(employer, {"$set": {"status": "done"}})


@bot.message_handler(content_types=["text"], func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'condidate'
                                                                  and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'done')
def pollCreateResume(message):
    employer = config.db.find({"chat_id": message.chat.id})[0]

    if employer['level'] == 'getCompany':
        config.db.update_one(employer, {"$set": {"level": "getPosition", "company": message.text}})
        bot.send_message(message.chat.id, 'Укажите должность которую вы занимали:')
    elif employer['level'] == 'getPosition':
        config.db.update_one(employer, {"$set": {"level": "getExperience", "position": message.text}})
        bot.send_message(message.chat.id, 'Укажите ваши результаты и достяжения:')
    elif employer['level'] == 'getExperience':
        config.db.update_one(employer, {"$set": {"level": "getResults", "experience": message.text}})
        bot.send_message(message.chat.id, 'Укажите причину увольнения:')
    elif employer['level'] == 'getResults':
        config.db.update_one(employer, {"$set": {"level": "getReason", "results": message.text}})
        bot.send_message(message.chat.id, 'Укажите типовые задачи, которые должен будет выполнять Ваш сотрудник (в одном сообщении):')
    elif employer['level'] == 'getReason':
        config.db.update_one(employer, {"$set": {"level": "", "reason": message.text}})

        sendCreateResume(message)

        markup = keyboardMenuCondidate()
        bot.send_message(message.chat.id, 'Вы создали свое резюме...', reply_markup=markup)

if __name__ == '__main__':
    bot.polling()
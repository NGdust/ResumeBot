import json
import time

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

def AK47(LEVEL, message):
    user = config.db.find({"chat_id": message.chat.id})[0]
    for i, v in LEVEL.items():
        if user['level'] == v['method']:
            next_level = LEVEL[i+1]
            logger.info(f"{user['chat_id']} -> method {next_level['method']}")
            config.db.update_one(user, {"$set": {"status": v['status'], "level": next_level['method'], v['method']: message.text}})
            if next_level['tip']:
                bot.send_message(message.chat.id, next_level['tip'])
            if next_level['status'] == "done":
                user = config.db.find({"chat_id": message.chat.id})[0]
                return user, True
    return user, False


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
        config.db.insert_one({"chat_id": message.chat.id, "username": message.from_user.username})
        user = config.db.find({"chat_id": message.chat.id})[0]

    if 'type' not in user or user['type'] == None or user['type'] == "":
        logger.info("User doesn't has type")
        bot.send_message(message.chat.id, 'Привет, я бот созданный для ....', reply_markup=keyboardStart())
        config.db.update_one(user, {"$set": {"status": "reg", "type": ''}})
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
        logger.info(f"delete account")
        user = config.db.find({"chat_id": message.chat.id})[0]
        config.db.delete_one(user)
        data = {
            "username": user['username'],
        }
        requests.post(config.HOST + config.USER_API + 'delete', data=data)
        bot.send_message(message.chat.id, 'Ваша учетная запись удалена')
    except:
        bot.send_message(message.chat.id, 'Вы еще не зарегистрировались', reply_markup=keyboardStart())


@bot.callback_query_handler(func=lambda call: True)
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

        if call.data == "create_vacansy":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="На какую должность:")
            config.db.update_one(user, {"$set": {"level": "getPosition"}})
        if call.data == "create_resume":
            data = {
                "username": user['username'],
            }
            responce = requests.post(config.HOST + config.DATA_API + 'resumes', data=data)
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
            responce = requests.post(config.HOST + config.DATA_API + 'vacansies', data=data)
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
            responce = requests.post(config.HOST + config.DATA_API + 'resumes', data=data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,  text="Ваши резюме: ")
            resumes = json.loads(responce.text)
            for item in resumes:
                text = f"Компания: {item['company']}\n" \
                       f"Должность: {item['position']}\n" \
                       f"Опыт: {item['experience']}\n" \
                       f"Причина увольнения: {item['reason']}\n" \
                       f"Результаты/достяжения: {item['results']}"
                bot.send_message(call.message.chat.id, text=text)


@bot.message_handler(content_types=["text"],
                     func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'employer'
                                          and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegEmployer(message):
    employer, end = AK47(LEVEL_EMPLOYER, message)
    if end:
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
        requests.post(url=config.HOST + config.USER_API + 'create/employer', data=data)

        bot.send_message(message.chat.id,
                         'Спасибо за регистрацию. Теперь вы можете создавать вакансии',
                         reply_markup=keyboardMenuEmployer())




@bot.message_handler(content_types=["text"],
                     func=lambda message: config.db.find({"chat_id": message.chat.id})[0]['type'] == 'condidate'
                                          and config.db.find({"chat_id": message.chat.id})[0]['status'] == 'reg')
def pollRegCandidat(message):
    candidat, end = AK47(LEVEL_CANDIDAT, message)
    if end:
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
        requests.post(url=config.HOST + 'create/condidate', data=data)
        bot.send_message(message.chat.id,
                         'Спасибо за регистрацию. Теперь вы можете создавать резюму',
                         reply_markup=keyboardMenuCondidate())


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

        markup = keyboardMenuEmployer()
        bot.send_message(message.chat.id, 'Вы создали свою вакансию...', reply_markup=markup)


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

        markup = keyboardMenuCondidate()
        bot.send_message(message.chat.id, 'Вы создали свое резюме...', reply_markup=markup)



if __name__ == '__main__':
    bot.polling()

import json
import requests
import telebot
from telebot import types
from database import DB
from keyboards import keyboardMenuEmployer, keyboardMenuCondidate, keyboardStart


bot = telebot.TeleBot('1349245843:AAE7ffXUwG7iPWAvui3IRhagNrFqhZ7JGVA')
db = DB("localhost", 27017).db
print(' [X] START TELEGRAM BOT')
db.insert_one({"chat_id": 0, 'level': '', 'type': ''})

class User:
    def __init__(self, message, user):
        self.message = message
        self.user = user
        db.update_one(self.user, {"$set": {"username": self.message.from_user.username, "chat_id": message.chat.id}})
        self.host = 'http://127.0.0.1:8000/api/v1/user/'

    def getFAQ(self):
        pass

    def clearData(self, data):
        data.pop('_id')
        data.pop('level')
        data.pop('type')
        for k, v in data.items():
            try:
                data[k] = v.replace("['", '').replace("']", '')
            except AttributeError:
                continue
        return data

    def sendServer(self, url):
        print(self.user)
        data = self.clearData(self.user)
        responce = requests.post(url=self.host + url, data=data)
        responce = json.loads(responce.text)
        if 'error' in responce:
            bot.send_message(self.message.chat.id, responce['error'])

class RegEmployer(User):
    def __init__(self, message, user):
        super(RegEmployer, self).__init__(message, user)

        self.registration()

    def menuEmployer(self):
        markup = keyboardMenuEmployer()
        bot.send_message(self.message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать вакансии', reply_markup=markup)

    def registration(self):
        if self.user['level'] == 'getCompany':
            db.update_one(self.user, {"$set": {"level": "getCategory", "company": self.message.text}})
            bot.send_message(self.message.chat.id, 'Укажите профиль деятельности:')
        elif self.user['level'] == 'getCategory':
            db.update_one(self.user, {"$set": {"level": "getAddress", "category": self.message.text}})
            bot.send_message(self.message.chat.id, 'Укажите адрес:')
        elif self.user['level'] == 'getAddress':
            db.update_one(self.user, {"$set": {"level": "getFio", "address": self.message.text}})
            bot.send_message(self.message.chat.id, 'ФИО контактного лица:')
        elif self.user['level'] == 'getFio':
            db.update_one(self.user, {"$set": {"level": "getPhone", "fio": self.message.text}})
            bot.send_message(self.message.chat.id, 'Контактный номер телефона:')
        elif self.user['level'] == 'getPhone':
            db.update_one(self.user, {"$set": {"level": "getEmail", "phone": self.message.text}})
            bot.send_message(self.message.chat.id, 'Почта:')
        elif self.user['level'] == 'getEmail':
            db.update_one(self.user, {"$set": {"level": "getUrl", "email": self.message.text}})
            bot.send_message(self.message.chat.id, 'URL:')
        elif self.user['level'] == 'getUrl':
            db.update_one(self.user, {"$set": {"level": "wait", "url": self.message.text}})
            self.sendServer('create/employer/')
            self.menuEmployer()


class RegCondidate(User):
    def __init__(self, message, user):
        super(RegCondidate, self).__init__(message, user)

        self.registration()

    def menuEmployer(self):
        markup = keyboardMenuCondidate()
        bot.send_message(self.message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать резюму', reply_markup=markup)

    def createResume(self):
        pass

    def registration(self):
        if self.user['level'] == 'getName':
            db.update_one(self.user, {"$set": {"level": "getSecondName", "name": self.message.text}})
            bot.send_message(self.message.chat.id, 'Фамилия:')
        if self.user['level'] == 'getSecondName':
            db.update_one(self.user, {"$set": {"level": "getAge", "secondname": self.message.text}})
            bot.send_message(self.message.chat.id, 'Возраст:')
        if self.user['level'] == 'getAge':
            db.update_one(self.user, {"$set": {"level": "getAddress", "age": self.message.text}})
            bot.send_message(self.message.chat.id, 'Адресс:')
        if self.user['level'] == 'getAddress':
            db.update_one(self.user, {"$set": {"level": "getEmail", "address": self.message.text}})
            bot.send_message(self.message.chat.id, 'Email:')
        if self.user['level'] == 'getEmail':
            db.update_one(self.user, {"$set": {"level": "getPhone", "email": self.message.text}})
            bot.send_message(self.message.chat.id, 'Телефон:')
        if self.user['level'] == 'getPhone':
            db.update_one(self.user, {"$set": {"level": "getUrl", "phone": self.message.text}})
            bot.send_message(self.message.chat.id, 'Cсылка на соц. сети:')
        elif self.user['level'] == 'getUrl':
            db.update_one(self.user, {"$set": {"level": "wait", "url": self.message.text}})
            self.sendServer('create/condidate/')
            self.menuEmployer()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот созданный для ....', reply_markup=keyboardStart())

@bot.message_handler(commands=['menu'])
def start_message(message):
    user = db.find({"chat_id": message.chat.id})[0]
    if not user:
        bot.send_message(message.chat.id, 'Извините, вы еще не прошли регистрацию')
    else:
        if user['type'] == 'employer':
            bot.send_message(message.chat.id, 'Главное меню работодателя!', reply_markup=keyboardMenuEmployer())
        elif user['type'] == 'condidate':
            bot.send_message(message.chat.id, 'Главное меню соискателя!', reply_markup=keyboardMenuCondidate())

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    checkDB = db.count_documents({"chat_id": call.message.chat.id})

    if call.message:
        if call.data == "employer":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="В какой компании вы работаете:")
            if checkDB == 0:
                db.insert_one({"chat_id": call.message.chat.id, "level": "getCompany", "type": call.data})
            else:
                db.update_one(db.find({"chat_id": call.message.chat.id})[0], {"$set": {"level": "getCompany", "type": call.data}})
        if call.data == "condidate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Имя:")
            if checkDB == 0:
                db.insert_one({"chat_id": call.message.chat.id, "level": "getName", "type": call.data})
            else:
                db.update_one(db.find({"chat_id": call.message.chat.id})[0], {"$set": {"level": "getName", "type": call.data}})


@bot.message_handler(content_types=["text"])
def handle_message_keyboard(message):
    checkDB = db.count_documents({"chat_id": message.chat.id})
    if checkDB != 0:
        user = db.find({"chat_id": message.chat.id})[0]
        if user['type'] == 'employer':
            RegEmployer(message, user)
        elif user['type'] == 'condidate':
            RegCondidate(message, user)


bot.polling()
import json
import requests
import telebot
from telebot import types
from database import DB


bot = telebot.TeleBot('1349245843:AAE7ffXUwG7iPWAvui3IRhagNrFqhZ7JGVA')
db = DB("localhost", 27017).db
print(' [X] START TELEGRAM BOT')


class User:
    def __init__(self, message, user):
        self.message = message
        self.user = user
        db.update_one(self.user, {"$set": {"username": self.message.from_user.username}})
        self.host = 'http://127.0.0.1:8000/api/v1/user/'

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

        self.generateMsg()

    def menuEmployer(self):
        markup = types.InlineKeyboardMarkup()
        create_vacansy = types.InlineKeyboardButton(text='Создать заявку', callback_data='create_vacansy')
        vacansies = types.InlineKeyboardButton(text='Мои вакансии', callback_data='vacansies')
        faq = types.InlineKeyboardButton(text='FAQ', callback_data='faq')
        markup.add(create_vacansy)
        markup.add(vacansies)
        markup.add(faq)
        bot.send_message(self.message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать вакансии', reply_markup=markup)

    def generateMsg(self):
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

        self.generateMsg()

    def menuEmployer(self):
        markup = types.InlineKeyboardMarkup()
        create_resume = types.InlineKeyboardButton(text='Создать резюме', callback_data='create_resume')
        resumes = types.InlineKeyboardButton(text='Мои резюме', callback_data='resumes')
        faq = types.InlineKeyboardButton(text='FAQ', callback_data='faq')
        markup.add(create_resume)
        markup.add(resumes)
        markup.add(faq)
        bot.send_message(self.message.chat.id, 'Спасибо за регистрацию. Теперь вы можете создавать резюму', reply_markup=markup)

    def generateMsg(self):
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
    markup = types.InlineKeyboardMarkup()
    employer = types.InlineKeyboardButton(text='Работодатель', callback_data='employer')
    condidate = types.InlineKeyboardButton(text='Соискатель', callback_data='condidate')
    markup.add(employer)
    markup.add(condidate)
    bot.send_message(message.chat.id, 'Привет, я бот созданный для ....', reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "employer":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="В какой компании вы работаете:")
            if not db.find({"chat_id": call.message.chat.id}):
                db.insert_one({"chat_id": call.message.chat.id, "level": "getCompany", "type": call.data})
            else:
                db.update_one(db.find({"chat_id": call.message.chat.id})[0], {"$set": {"level": "getCompany", "type": call.data}})
        if call.data == "condidate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Имя:")
            if not db.find({"chat_id": call.message.chat.id}):
                db.insert_one({"chat_id": call.message.chat.id, "level": "getName", "type": call.data})
            else:
                db.update_one(db.find({"chat_id": call.message.chat.id})[0], {"$set": {"level": "getName", "type": call.data}})


@bot.message_handler(content_types=["text"])
def handle_message_keyboard(message):
    user = db.find({"chat_id": message.chat.id})[0]
    if user['type'] == 'employer':
        RegEmployer(message, user)
    elif user['type'] == 'condidate':
        RegCondidate(message, user)


bot.polling()
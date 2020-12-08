from telebot import types


def keyboardStart():
    markup = types.InlineKeyboardMarkup()
    employer = types.InlineKeyboardButton(text='Работодатель', callback_data='employer')
    condidate = types.InlineKeyboardButton(text='Соискатель', callback_data='condidate')
    markup.add(employer)
    markup.add(condidate)
    return markup

def keyboardMenuEmployer():
    markup = types.InlineKeyboardMarkup()
    create_vacansy = types.InlineKeyboardButton(text='Создать заявку', callback_data='create_vacansy')
    vacansies = types.InlineKeyboardButton(text='Мои вакансии', callback_data='vacansies')
    faq = types.InlineKeyboardButton(text='FAQ', callback_data='faq')
    markup.add(create_vacansy)
    markup.add(vacansies)
    markup.add(faq)
    return markup

def keyboardMenuCondidate():
    markup = types.InlineKeyboardMarkup()
    create_resume = types.InlineKeyboardButton(text='Создать резюме', callback_data='create_resume')
    resumes = types.InlineKeyboardButton(text='Мои резюме', callback_data='resumes')
    faq = types.InlineKeyboardButton(text='FAQ', callback_data='faq')
    markup.add(create_resume)
    markup.add(resumes)
    markup.add(faq)
    return markup

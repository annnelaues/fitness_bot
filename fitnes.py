import telebot
from telebot import types
token = '1433761514:AAEjloVnA7U0E2ZflljiGYViTCgv0DGdnhc'
start, name, weight, height, sex, CONFIRMATION,res = range(7)
bot = telebot.TeleBot(token)

from collections import defaultdict
info_state = defaultdict(lambda: start)

def get_state(message):
    return info_state[message.chat.id]
def update_state(message, state):
    info_state[message.chat.id] = state
person_info = defaultdict(lambda: {})
def update_info(user_id, key, value):
   person_info[user_id][key] = value
def get_info(user_id):
    return person_info[user_id]
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item11 = types.KeyboardButton("женский")
item22 = types.KeyboardButton("мужской")
markup1.add(item11, item22)
markup1_close=types.ReplyKeyboardRemove()
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("даа,хочу")
item2 = types.KeyboardButton("неее,спасибо")
markup.add(item1, item2)
markup_close=types.ReplyKeyboardRemove()
@bot.message_handler(commands=['motivation'])
def handle_mot(message):
    bot.send_message(message.chat.id, text="https://www.woman.ru/health/diets/article/81412/")
    bot.send_message(message.chat.id, text="https://www.youtube.com/watch?v=ux6yDvS3PXw")
@bot.message_handler(commands=['about'])
def handle_mot(message):
    bot.send_message(message.chat.id, text="Я{0.first_name}. Я помогу помочь расcчитать твой идельный вес. Могу помочь похудеть если у тебя перевес или же набрать если недовес. А еще у меня есть команда  /motivation ".format(bot.get_me()))

@bot.message_handler(func=lambda message: get_state(message) == start)
def handle_message(message):
    bot.send_message(message.chat.id, text='Ваше имя')
    update_state(message, name)

@bot.message_handler(func=lambda message: get_state(message) == name)
def handle_name(message):
    update_info(message.chat.id, 'name', message.text)
    bot.send_message(message.chat.id, text='Ваш вес')
    update_state(message, weight)

@bot.message_handler(func=lambda message: get_state(message) == weight)
def handle_weight(message):
    update_info(message.chat.id, 'weight', message.text)
    bot.send_message(message.chat.id, text='Ваш рост')
    update_state(message, height)
@bot.message_handler(func=lambda message: get_state(message) == height)
def handle_height(message):
    update_info(message.chat.id, 'height', message.text)
    bot.send_message(message.chat.id, text='Ваш пол',parse_mode='html',reply_markup=markup1)
    update_state(message, sex)
@bot.message_handler(func=lambda message: get_state(message) ==sex)
def handle_sex(message):
    update_info(message.chat.id, 'sex', message.text)
    bot.send_message(message.chat.id, text='Вы подтверждаете свои данные{}'.format(get_info(message.chat.id)), reply_markup=markup1_close)
    update_state(message, CONFIRMATION)
@bot.message_handler(func = lambda message : get_state(message)==CONFIRMATION)
def handle_wf(message):
    if 'да' in message.text.lower():
        sex=person_info[message.chat.id]['sex']
        w=person_info[message.chat.id]['weight']
        h=person_info[message.chat.id]['height']
        n=person_info[message.chat.id]['name']
        if sex=='женский':
            id_w=(int(h)- 110) * 1.15
            if id_w == int(w):
                bot.send_message(message.chat.id, text='{},поздравляю! У вас идеальный вес'.format(n))
                bot.send_message(message.chat.id, text='Хотите сохранить свой вес?', parse_mode='html',reply_markup=markup)
            elif id_w > int(w):
                bot.send_message(message.chat.id, text='{},к сожалению,у вас недовес. Для вас иделаьный вес {}'.format(n,id_w))
                bot.send_message(message.chat.id, text='Хотите набрать вес?', parse_mode='html',reply_markup=markup)
            elif id_w<int(w):
                bot.send_message(message.chat.id, text='{},к сожалению,у перевес.Для вас иделаьный вес {}'.format(n,id_w))
                bot.send_message(message.chat.id, text='Хотите сбросить вес?', parse_mode='html',reply_markup=markup)
        elif sex=='мужской':
            id_w=(int(h)- 100) * 1.15
            if id_w == int(w):
                bot.send_message(message.chat.id, text='{},поздравляю! У вас идеальный вес'.format(n))
                bot.send_message(message.chat.id, text='Хотите сохранить свою фигуру?', parse_mode='html',reply_markup=markup)
            elif id_w > int(w):
                bot.send_message(message.chat.id, text='{},к сожалению,у вас недовес.Для вас иделаьный вес {}'.format(n,id_w))
                bot.send_message(message.chat.id, text='Хотите набрать вес?', parse_mode='html',reply_markup=markup)
            elif id_w<int(w):
                bot.send_message(message.chat.id, text='{},к сожалению,у перевес.Для вас иделаьный вес {}'.format(n,id_w))
                bot.send_message(message.chat.id, text='Хотите сбросить вес?', parse_mode='html',reply_markup=markup)
    update_state(message, res)
@bot.message_handler(func = lambda message : get_state(message)==res)
def handle_res(message):
    if 'даа,хочу' == message.text:
        markup2=types.InlineKeyboardMarkup(row_width=2)
        but1=types.InlineKeyboardButton("Упражнения", callback_data='ex')
        but2=types.InlineKeyboardButton("Диета", callback_data='di')
        markup2.add(but1,but2)
        bot.send_message(message.chat.id, text='C чего начнем?', parse_mode='html', reply_markup=markup2)
    elif "неее,спасибо"== message.text:
        bot.send_message(message.chat.id, text='Жаль( Если передумаешь,буду ждать здесь')
    update_state(message, start)
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
            if call.message:
                if call.data == 'ex':
                    markup3 = types.InlineKeyboardMarkup(row_width=2)
                    but11 = types.InlineKeyboardButton("для всего тела", callback_data='full')
                    but22 = types.InlineKeyboardButton("для красивых ног", callback_data='leg')
                    but3 = types.InlineKeyboardButton("для тонкой талии", callback_data='tal')
                    but4 = types.InlineKeyboardButton("для плоского живота", callback_data='jiv')
                    markup3.add(but11, but22, but3,but4)
                    bot.send_message(call.message.chat.id, text='Для какой части тело хочешь получить упражнение?', parse_mode='html', reply_markup=markup3)
                    bot.send_message(call.message.chat.id, text="Вы также можете посетить наш фитнес клуб. Узнать про нас можете переходя по ссылке https://invictusfitness.kz/")
                    bot.send_location(call.message.chat.id,43.2048869,76.8970043 )
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='U can')
                elif call.data == 'di':
                    markup4 = types.InlineKeyboardMarkup(row_width=2)
                    but111 = types.InlineKeyboardButton("Завтрак", callback_data='br')
                    but222 = types.InlineKeyboardButton("Обед", callback_data='lun')
                    but33 = types.InlineKeyboardButton("Ужин", callback_data='din')
                    markup4.add(but111, but222, but33)
                    bot.send_message(call.message.chat.id, text='Какой рецепт хочешь получить?',parse_mode='html', reply_markup=markup4)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='U can')
                elif call.data == 'br':
                    bot.send_message(call.message.chat.id, text="https://www.youtube.com/watch?v=AIU-wpOzOwc")
                elif call.data == 'lun':
                    bot.send_message(call.message.chat.id,text="https://www.fitnessera.ru/podbiraem-pravilnyj-obed-dlya-poxudeniya-chto-sest-pri-diete.html")
                elif call.data == 'din':
                    bot.send_message(call.message.chat.id, text="https://glamusha.ru/dietplan/1990.html")
                elif call.data == 'full':
                    bot.send_message(call.message.chat.id, text="https://www.youtube.com/watch?v=CGmr02bfHUo")
                elif call.data == 'leg':
                    bot.send_message(call.message.chat.id, text="https://www.youtube.com/watch?v=EUruBzhv7Kk")
                elif call.data == 'tal':
                    bot.send_message(call.message.chat.id, text="https://www.youtube.com/watch?app=desktop&v=cIuiQyfKBTg")
                elif call.data == 'jiv':
                    bot.send_message(call.message.chat.id, text="https://www.youtube.com/watch?v=rPPu5RqB_TU")
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Good luck')
bot.polling()
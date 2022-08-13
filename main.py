import telebot
import os
import logging
from telebot import types
from deepface import DeepFace


PORT = int(os.environ.get('PORT', 5000))

TOKEN = '5398572755:AAG2j8S0M_OY71TrlWv1dZx0hBgx2lFruZ4'
bot = telebot.TeleBot(TOKEN)
IDEAS_ID = "-1001756194402" #узнать можно этим же ботом

#flags:
Flag = False
checker = False
secondWaiter = False
ready = False

#text:
jobtext = '/Cотрудничество'
ideaText = '/Идея'
NaviText = '/Навигатор'
EnterText = '/Готово'
TestText = '/Тест'

#links:
urlCh ="https://www.youtube.com/channel/UCCO8KsSH45_YMF0coYFY89Q"
urlVK ="https://vk.com/developmentaksakalov"
urlTT ="https://www.tiktok.com/@ivan__smit?lang=ru-RU"
urlTG = "https://t.me/ivansmittt"

@bot.message_handler(commands=['start','info'])
def start(message):
    mess = f'Привет,  {message.from_user.first_name}' + "\nДанный бот создан для облегчения связи с аудиторией, " \
                                                        "так как среднестатистический подписчик, как правило, хочет " \
                                                        "связаться по поводу одной из тем, представленных ниже. " \
                                                        "Если ты один из таких, то добро пожаловать)"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    job = types.KeyboardButton(jobtext)
    idea = types.KeyboardButton(ideaText)
    navi = types.KeyboardButton(NaviText)
    markup.add(idea, job, navi)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(commands=['назад','help','info'])
def start(message):
    mess = f'{message.from_user.first_name}, вот что умеет бот:' + "\n\n/Идея - предложить свою(или чужую) идею/наработки/статью(хоть с хабра)\n\n" \
                                                        "/Сотрудничество - по вопросам покупки/разработки на заказ/рекламы/чего-то ещё\n\n" \
                                                        "/Навигатор - все медиаресурсы которые +- активно ведутся"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    job = types.KeyboardButton(jobtext)
    idea = types.KeyboardButton(ideaText)
    navi = types.KeyboardButton(NaviText)
    markup.add(idea, job, navi)
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler(commands=['pass'])
def getuser(message):
    bot.send_message(message.chat.id, message.from_user.id*37, parse_mode='html')


@bot.message_handler(commands=['chat'])
def getuser(message):
    bot.send_message(message.chat.id, message.chat.id, parse_mode='html')

@bot.message_handler(commands=['Готово'])
def all_messages(message):
    mess = message.text
    bot.send_message(message.chat.id, "Зачем ты написал " +mess +"?", parse_mode='html')
    bot.forward_message(IDEAS_ID, message.chat.id, message.message_id)

@bot.message_handler(commands=['Cотрудничество', 'Навигатор', 'Идея'])
def navigateButtons(message):
    if message.text == jobtext:
        bot.delete_my_commands()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Написать сообщение", url="https://vk.com/im?sel=-132621744"))
        bot.send_message(message.chat.id, "Наша рабочая группа в VK: \n "
                                          "https://vk.com/auxiliumexo", reply_markup=markup)
    elif message.text == ideaText:
        bot.delete_my_commands()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        website = types.KeyboardButton("/Видео")
        text = types.KeyboardButton("/Текст")
        photo = types.KeyboardButton("/Фото")
        back = types.KeyboardButton("/назад")
        markup.add(back, website, text, photo)
        bot.send_message(message.chat.id, "Воу, а ты я смотрю выдумщик и хочешь поделиться своей идеей! Но для начала выбери то, в какой форме ты хочешь прислать её нам:", reply_markup=markup)

    elif message.text == NaviText:
        bot.delete_my_commands()
        markup =types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("YouTube", url=urlCh))
        markup.add(types.InlineKeyboardButton("VK", url=urlVK))
        markup.add(types.InlineKeyboardButton("TT", url=urlTT))
        markup.add(types.InlineKeyboardButton("Telegram (ну мало ли)", url=urlTG))
        bot.send_message(message.chat.id, "Вот ссылки на все актуальные соцсети, не теряй", reply_markup=markup)


@bot.message_handler(commands=["Тест"])
def faseID(message):
    global checker
    checker = True
    mess = f'Добро пожаловать в секретную функцию этого бота! Данный алгоритм - распознавание лиц - будет почти без изменений находиться в новом шлеме экзоскелета, который мы сейчас создаем. ' \
           f'Лица будут распознаваться с помощью настоящего искусственного интеллекта, все по взрослому😎\n\n' \
           f'Отправь  <b><u>ОДНО ФОТО</u></b>  лица человека  <b><u>БЕЗ ПОДПИСЕЙ</u></b>  и следуй дальнейшим инструкциям\n\n' \
           f'Еще важно чтобы фото было четкое, как на паспорт, чтобы нейросеть точно узнала в вас человека'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("/назад"))
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=["Текст","Видео","Фото"])
def navigateButtons(message):
    global  Flag
    if message.text == "/Текст":
        mess= f'Решил описать свою идею текстом? Чтож, ладно. Главное опиши ее \n\n<b><u>ОДНИМ СООБЩЕНИЕМ!</u></b>\n\n(можно и ссылкой)'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("/назад"))
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        Flag = True
        sendText(message)

    elif message.text == "/Видео":
        mess = "Пришли видео которым хочешь поделиться.Важно,чтобы оно было без описания и \n\n<b>за один раз можно <u>ТОЛЬКО ОДНО!</u></b>"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("/назад"))
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        Flag = True

    elif message.text == "/Фото":
        mess =f'Давай, жду фоточек от тебя.Важно, чтобы она была без описания и \n\n<b>за один раз можно <u>ТОЛЬКО ОДНУ</u></b>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("/назад"))
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        Flag = True
    else:
        bot.send_message(message.chat.id, "Неизвестная команда")


@bot.message_handler(content_types=['text'])
def sendText(message):
    global Flag
    mess = f'Спасибо, {message.from_user.first_name}!'+"\n\nМы обязательно прочитаем твое предложение, и свяжемся, если нам понадобятся подробности!"
    if message.text !='/Текст':
        if message.text !='/Видео':
            if message.text !='/Фото':
                if  Flag == True:
                    bot.send_message(message.chat.id, mess, parse_mode='html')
                    bot.send_message(IDEAS_ID, f'<b>Текст от <u>{message.from_user.first_name}</u></b> @{message.from_user.username} \n\n' + message.text,parse_mode='html')
                    Flag = False


@bot.message_handler(content_types=['photo'])
def checkFaces(message):
    global checker
    global secondWaiter
    global ready
    global Flag

    if secondWaiter == True:
        number = 'Two'
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        downloaded_photo = bot.download_file(file_info.file_path)
        scr = 'photos/' + 'faceID' + number + file_extension
        with open(scr, 'wb') as new_file:
            new_file.write(downloaded_photo)

        bot.reply_to(message, 'Второе фото получено, ожидайте ответа.\nНейросеть иногда долго думает)')
        bot.send_message(IDEAS_ID,f'<b>FaceId 2 от <u>{message.from_user.first_name}</u></b> @{message.from_user.username} \n\n',parse_mode='html')
        bot.send_photo(IDEAS_ID, message.photo[0].file_id)
        secondWaiter = False
        ready = True

    if checker == True:
        number = 'One'
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        downloaded_photo = bot.download_file(file_info.file_path)
        scr = 'photos/' + 'faceID' + number + file_extension
        with open(scr, 'wb') as new_file:
            new_file.write(downloaded_photo)

        bot.reply_to(message,'Первое фото лица получено')
        bot.send_message(message.chat.id, 'Теперь пришлите второе фото', parse_mode='html')
        bot.send_message(IDEAS_ID,f'<b>FaceId 2 от <u>{message.from_user.first_name}</u></b> @{message.from_user.username} \n\n',parse_mode='html')
        bot.send_photo(IDEAS_ID, message.photo[0].file_id)
        checker = False
        secondWaiter = True


    if ready == True:
        answ = face_check('photos/faceIDOne.jpg', 'photos/faceIDTwo.jpg')
        Flag = False
        if answ == "лица одного и того же человека":
            bot.send_message(message.chat.id, 'Это лица одного и того же человека. Будь он в экзоскелете, ему был бы разрешён доступ)', parse_mode='html')
            ready = False
        elif answ == "хуй пойми кто это":
            bot.send_message(message.chat.id, 'Не обнаружено ничего общего, это разные люди', parse_mode='html')
            ready = False
        elif answ == "err":
            bot.send_message(message.chat.id, 'Что-то пошло не так, возможно лицо на фото не распозналось из-за фильтров/освещения/ракурса\n'
                                              'жми "/назад"', parse_mode='html')
            ready = False
        else:
            bot.send_message(message.chat.id, 'Что-то вообще очень сильно пошло не так, срочно пишите админу', parse_mode='html')
            ready = False


    mess = f'Спасибо, {message.from_user.first_name}!' + "\n\nВозможно, это будет служить вдохновением для какого-нибудь из дальнейших проектов"
    if (Flag == True)&(ready == False)&(checker == False)&(secondWaiter == False):
        bot.send_message(message.chat.id, mess, parse_mode='html')
        bot.send_message(IDEAS_ID,
                         f'<b>Фото от <u>{message.from_user.first_name}</u></b> @{message.from_user.username} \n\n',
                         parse_mode='html')
        bot.send_photo(IDEAS_ID, message.photo[0].file_id)


def face_check(img1, img2):
    try:
        resultDick = DeepFace.verify(img1_path=img1, img2_path=img2)
        if resultDick.get('verified'):
            return ("лица одного и того же человека")
        else:
            return ("хуй пойми кто это")
    except Exception as _ex:
        return "err"



@bot.message_handler(content_types=['video'])
def sendPhoto(message):
    global Flag
    mess = f'Спасибо, {message.from_user.first_name}!' + "\n\nВозможно, здесь мы найдем новые идеи для дальнейших проектов"
    if Flag == True:
        bot.send_message(message.chat.id, mess, parse_mode='html')
        bot.send_message(IDEAS_ID,f'<b>Видео от <u>{message.from_user.first_name}</u></b> @{message.from_user.username} \n\n',parse_mode='html')
        bot.send_video(IDEAS_ID, message.video.file_id)

bot.polling(none_stop=True)
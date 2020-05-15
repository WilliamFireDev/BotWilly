from bot import *
import db
import keyboards
import horoscope_parser

@bot.message_handler(commands=["developer"])
def who_developer(message):
    bot.send_message(message.chat.id, "t.me/mrfire7")

@bot.message_handler(commands=["channel"])
def who_developer(message):
    bot.send_message(message.chat.id, "Наш канал t.me/Horoskope_Willy")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, '''
        Привет, <b>{0.first_name}</b>!Я <i>Бот Willy-гороскоп</i>. Чтобы посмотреть гороскоп просто используйте команду /start .

        /channel - Канал бота
        /developer - Создатель'''.format(message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(commands=["start"])
def start_handler(message):
    if not db.Users().exists(message.chat.id):
        db.Users().add(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Выберите знак зодиака", reply_markup=keyboards.inline_horoscope)
    db.Users().update_interface_state(message.chat.id, 0)


@bot.message_handler(commands=["post"], func=lambda message: message.chat.id == config.BOT_ADMIN_ID)
def post_handler(message):
    msg = bot.send_message(message.chat.id, "Что отправлять?")
    bot.register_next_step_handler(msg, send_post)


@bot.callback_query_handler(func=lambda callback: callback.data in keyboards.HOROSCOPE.values())
def callback_handler(callback):
    bot.delete_message(callback.from_user.id, callback.message.message_id)
    bot.send_message(callback.from_user.id, horoscope_parser.get_today(callback.data),
                     reply_markup=keyboards.inline_horoscope)


def send_post(message):
    for user in db.Users():
        try:
            bot.forward_message(user.user_id, message.chat.id, message.message_id)
        except:
            bot.send_message(message.chat.id, f"Не удалось отправить пост пользователю @{user.user_name}")

@bot.message_handler(content_types=['text'])
def text_help (message):
    bot.send_message(message.chat.id,  "Шо? Доступные команды: /help ") 

@bot.message_handler(content_types=['pinned_message', 'delete_chat_photo', 'supergroup_chat_created', 'left_chat_member', 'new_chat_members', 'new_chat_title', 'group_chat_created'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, "Вы сегодня свой гороскоп чекнули? /start ")

def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
import extension as exten

bot = telebot.TeleBot(config.token)
users = {}
sudo_password = "IMADMIN"

@bot.message_handler(commands=['start'])
def send_welcome(message):
       # Создаем инлайн-клавиатур
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Начать", callback_data='start'))
    bot.send_message(message.chat.id, text=config.init_message, reply_markup=keyboard)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query_main(call):

    user_id = call.message.chat.id
    if user_id not in users:
        users[user_id] = []

    if call.data == 'start':
        users[user_id] = []
        keyboard_init = InlineKeyboardMarkup()
        keyboard_init.row(InlineKeyboardButton("Записаться на экзамен", callback_data='group_rec'))
        keyboard_init.row(InlineKeyboardButton("For admins", 
                                               callback_data='for_admins'))
        bot.send_message(call.message.chat.id, text='Выберите действие', reply_markup=keyboard_init)

    if call.data.startswith('group_rec'):
        keyboard_record1 = exten.create_keyboard_from_dir(dirname='list_student', 
                                                         callback='exam_rec')
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Отлично! Выбери группу на запись", reply_markup=keyboard_record1)
        
    if call.data.startswith('for_admins'):
        keyboard_foradmins1 = InlineKeyboardMarkup()
        keyboard_foradmins1.row(InlineKeyboardButton("Очистить данные с предыдущего семестра", 
                                                     callback_data='clean_alldata'))
        keyboard_foradmins1.row(InlineKeyboardButton("Посмотреть списки экзаменуемых и время", 
                                                     callback_data='for_teach'))
        keyboard_foradmins1.row(InlineKeyboardButton("Изменить расписание и время экзаменов", 
                                                     callback_data='change_exam_list_for_groups'))
        keyboard_foradmins1.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Вы вошли в режим админа. Выберите действие", 
                            reply_markup=keyboard_foradmins1)
        

    if call.data.startswith('for_teach'):
        keyboard_record2 = exten.create_keyboard_from_dir(dirname='list_student',  
                                                       callback='teach_watch_subject')
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Отлично! Выберите группу чтобы просмотреть список", 
                            reply_markup=keyboard_record2)

    if call.data.startswith('teach_watch_subject'):
        substring = call.data[len("teach_watch_subject_"):]
        users[user_id].append(substring)
        keyboard_record22 = exten.create_object_from_db(to_return='keyboard', 
                                                        column_name='Экзамен', 
                                                        callback='teach_watch_group',
                                                        group=users[user_id][0])
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Вы выбрали группу {users[user_id][0]}. Выберите экзамен для просмотра", 
                                reply_markup=keyboard_record22)
    
    if call.data.startswith('change_exam_list_for_groups'):
        keyboard_foradmins3 = InlineKeyboardMarkup()
        keyboard_foradmins3.row(InlineKeyboardButton("Очистить все очереди", 
                                                     callback_data='clean_queue'))
        keyboard_foradmins3.row(InlineKeyboardButton("Добавить очередь на экзамен", 
                                                     callback_data='add_queue'))
        keyboard_foradmins3.row(InlineKeyboardButton("Удалить очередь на экзамен", 
                                                     callback_data='remove_queue'))
        keyboard_foradmins3.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Вы вошли в режим работы с очередями. Выберите действие", 
                            reply_markup=keyboard_foradmins3)
        

    if call.data.startswith('clean_queue'):
        keyboard_foradmins3 = InlineKeyboardMarkup()
        keyboard_foradmins3.row(InlineKeyboardButton('Отмена', callback_data='start'))
        keyboard_foradmins3.row(InlineKeyboardButton("Подтвердить", 
                                                     callback_data='r_all_queue'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                    message_id=call.message.message_id, 
                    text="Подтвердите удаление очередей", 
                    reply_markup=keyboard_foradmins3)

    if call.data.startswith('clean_queue'):
        exten.change_exam_list_for_groups(action='removeall_queues')
        keyboard_foradmins3 = InlineKeyboardMarkup()
        keyboard_foradmins3.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text="Все очереди удалены", 
            reply_markup=keyboard_foradmins3)
        
    if call.data.startswith('add_queue'):
        keyboard_addqueue = exten.create_keyboard_from_dir(dirname='list_student', 
                                                         callback='add_group_inqueue')
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Отлично! Выберите группу на добавление в очередь", 
                            reply_markup=keyboard_addqueue)
        
    if call.data.startswith('add_group_inqueue'):
        substring = call.data[len("add_group_inqueue_"):]
        users[user_id].append(substring)
        keyboard_foradmins2 = InlineKeyboardMarkup()
        keyboard_foradmins2.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Введите название предмета и время через пробел, например: Алгебра 14:00", 
                                reply_markup=keyboard_foradmins2)
        bot.register_next_step_handler(call.message, lambda msg: input_subject_time(msg, info=users[user_id]))

    if call.data.startswith('remove_queue'):
        keyboard_rqueue = exten.create_keyboard_from_dir(dirname='db_groups', 
                                                         callback='remove_groupqueue')
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Отлично! Выберите группу", 
                            reply_markup=keyboard_rqueue)

    if call.data.startswith('remove_groupqueue'):
        substring = call.data[len("remove_groupqueue_"):]
        users[user_id].append(substring)
        keyboard_rqueue = exten.create_object_from_db(to_return='keyboard', 
                                                         callback='remove_Ygroupqueue',
                                                         group=users[user_id][0]
                                                         )
        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.message_id, 
                            text="Отлично! Выберите очередь на удаление", 
                            reply_markup=keyboard_rqueue)    

    if call.data.startswith('remove_Ygroupqueue'):
        substring = call.data[len("remove_Ygroupqueue_"):]
        substring = substring.split('_')
        for item in substring:
            users[user_id].append(item)
        keyboard_foradmins2 = InlineKeyboardMarkup()
        keyboard_foradmins2.row(InlineKeyboardButton("Подтвердить", 
                                                     callback_data='remove_groupqueue_reset'))
        keyboard_foradmins2.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Подтвердите сброс очереди {users[user_id][1]}: {users[user_id][2]}", 
                                reply_markup=keyboard_foradmins2)
        
    if call.data.startswith('remove_groupqueue_reset'):
        exten.change_exam_list_for_groups(action='remove',
                                          group=users[user_id][0],
                                          exam=users[user_id][1],
                                          time=users[user_id][2])
        keyboard_foradmins5 = InlineKeyboardMarkup()
        keyboard_foradmins5.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Очередь успешно сброшена", 
                                reply_markup=keyboard_foradmins5)
        

    if call.data.startswith('clean_alldata'):
        keyboard_foradmins2 = InlineKeyboardMarkup()
        keyboard_foradmins2.row(InlineKeyboardButton("Подтвердить", 
                                                     callback_data='confirm_deleting'))
        keyboard_foradmins2.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Подтвердите сброс очередей", 
                                reply_markup=keyboard_foradmins2)
        
    if call.data.startswith('confirm_deleting'):
        keyboard_foradmins2 = InlineKeyboardMarkup()
        keyboard_foradmins2.row(InlineKeyboardButton('Домой', callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Введите пароль", 
                                reply_markup=keyboard_foradmins2)
        bot.register_next_step_handler(call.message, handle_password)
     
    if call.data.startswith('teach_watch_group'):
        substring = call.data[len("teach_watch_group_"):]
        list_students_exam = exten.watch_students(group=users[user_id][0],exam=substring)
        keyboard_record21 = InlineKeyboardMarkup()
        keyboard_record21.row(InlineKeyboardButton("Домой", callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, 
                              text=f'Конечно! Вот список записанных по времени на экзамен:\n\n{list_students_exam}',
                              reply_markup=keyboard_record21)

    if call.data.startswith('exam_rec'):
        substring = call.data[len("exam_rec_"):]
        users[user_id].append(substring)
        keyboard_record3 = exten.create_object_from_db(to_return='keyboard', 
                                                       column_name='Экзамен', 
                                                       callback='exam_time_rec',
                                                       group=users[user_id][0])
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Ты выбрал группу {users[user_id][0]}. Выбери на какой экзамен записаться", 
                                reply_markup=keyboard_record3)

    if call.data.startswith('exam_time_rec'):
        substring = call.data[len("exam_time_rec_"):]
        users[user_id].append(substring)
        keyboard_record4 = exten.create_object_from_db(to_return='keyboard', 
                                                       column_name='Время', 
                                                       exam=users[user_id][1], 
                                                       callback='name_rec', group=users[user_id][0])
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Ты выбрал экзамен {users[user_id][1]}. Выбери время записи", 
                                reply_markup=keyboard_record4)

    if call.data.startswith('name_rec'):
        substring = call.data[len("name_rec_"):]
        users[user_id].append(substring)
        students = exten.get_students(users[user_id][0])
        keyboard_record5 = exten.create_keyboard_from_list(students, callback='prepare_to_record')
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Ты выбрал время {users[user_id][2]}. Выбери себя, чтобы записаться", 
                                reply_markup=keyboard_record5)
        
    if call.data.startswith('prepare_to_record'):
        substring = call.data[len("prepare_to_record_"):]
        users[user_id].append(substring)
        keyboard_record6 = InlineKeyboardMarkup()
        keyboard_record6.row(InlineKeyboardButton("Подтвердить", callback_data='record_to_final_list'))
        keyboard_record6.row(InlineKeyboardButton("Отмена", callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text=f"Ты выбрал имя {users[user_id][3]}. Подтверди ввод в базу данных", 
                                reply_markup=keyboard_record6)

    if call.data == 'record_to_final_list':
        exten.final_record(users[user_id])
        keyboard_record7 = InlineKeyboardMarkup()
        keyboard_record7.row(InlineKeyboardButton("Домой", callback_data='start'))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, 
                              text='Вы успешно записались на экзамен',
                              reply_markup=keyboard_record7)
        
def handle_password(message):
    user_password = message.text

    if user_password == sudo_password:
        exten.clean_alldata()
        keyboard_clean_home = InlineKeyboardMarkup()
        keyboard_clean_home.row(InlineKeyboardButton("Домой", callback_data='start'))
        bot.send_message(chat_id=message.chat.id, 
                              text='Пароль верный. Все очереди успешно сброшены.',
                              reply_markup=keyboard_clean_home)
    else:
        keyboard_clean_home = InlineKeyboardMarkup()
        keyboard_clean_home.row(InlineKeyboardButton("Домой", callback_data='start'))
        bot.send_message(chat_id=message.chat.id,
                              text='Пароль неверный. Попробуйте снова',
                              reply_markup=keyboard_clean_home)

def input_subject_time(message,info):
    cortej = message.text.split()
    for item in cortej:
        info.append(item)
    exten.add_queue_group(info)
    keyboard_add_queue = InlineKeyboardMarkup()
    keyboard_add_queue.row(InlineKeyboardButton("Домой", callback_data='start'))
    bot.send_message(chat_id=message.chat.id,
                            text='Вы успешно добавили новую очередь',
                            reply_markup=keyboard_add_queue)


bot.polling()
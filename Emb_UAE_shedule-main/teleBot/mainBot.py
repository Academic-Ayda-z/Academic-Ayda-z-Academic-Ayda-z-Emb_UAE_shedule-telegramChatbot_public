from mainExtention import *
import threading
import sys
sys.path.append( '.' )
from b import checkLogin

'''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
'''
#url=Users/{update.effective_chat.username}-{update.effective_chat.id}
#pip install python-telegram-bot==13.13
updater = Updater(token)
dispatcher = updater.dispatcher


def newPayment(user):
    paymentsNofitications = user.paymentsNotifications


def addTeleBotUser(chat_id, username):
    newUser = TelegaBotUser(chat_id, username)
    checkPath(username, chat_id)
    allTeleBotUsersChatID[chat_id] = newUser
    usernamesChatId[username] = chat_id
    #wirte to files
    updateInfo()


def showMenueButtons():
    global allButtonsInAfterStartMenue
    buttons = [[KeyboardButton(i)] for i in allButtonsInAfterStartMenue]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return reply_markup


def showMenue(update: Update, context: CallbackContext):
    global allButtonsInAfterStartMenue

    addTeleBotUser(update.effective_chat.id, update.effective_chat.username)

    #print(update.effective_chat.username)
    #print(update.message.text)
    text = "برای مطلع شدن از چگونگی گرفتن وقت سفارت به شرایط و هزینه ها مراجعه کنید."

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=showMenueButtons())


def loginCheck(chatId):
    #make sure that all the info is there
    global allTeleBotUsersChatID
    user=allTeleBotUsersChatID[chatId]
    if user.email!='' and user.password!='' and user.desired_date[0] != '' and user.desired_date[1]!='' and user.location!='':

        result=checkLogin(chatId)

        if result:
            updateInfo()
            return True
    
    return False


def downloader(update: Update, context: CallbackContext):
    #insert the week to the path too
    path = f'Users/{update.effective_chat.username}-{update.effective_chat.id}'

    (context.bot.getFile(update.message.photo[-1].file_id)).download(
        f'{path}/{update.effective_chat.username}-{update.effective_chat.id}.png'
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='عکس دریافت شد. لطفا منتظر بمانید. با تشکر',
        reply_markup=showMenueButtons())

    forward_to_chat(update, context, message='photo')

    claimOfPaymen(update.effective_chat.username, update.effective_chat.id)


def agreeWithTermsButton(update: Update, context: CallbackContext):
    #now sending info about how to purches
    global allButtonsInAfterStartMenue, allTeleBotUsersChatID
    query = update.callback_query.data
    update.callback_query.answer()

    chat_id = update.effective_chat.id

    #user=allTeleBotUsersChatID[chat_id]

    if 'accepted The terms' in query:
        #send info about payment

        context.bot.send_photo(chat_id=chat_id,
                               photo=open('teter.png', 'rb'),
                               caption=" QRcode" + "\nERC20 شبکه")

        context.bot.send_message(chat_id=chat_id, text=getHasStrTxt())

        context.bot.send_message(chat_id=chat_id,
                                 text='لطفا عکس پرداخت را بفرستید.')


def chooseMenue(update: Update, context: CallbackContext):
    global allButtonsInAfterStartMenue, allInlinebuttons, allTeleBotUsersChatID, EMBInlineButtons, embLoc

    pricesAndPrincipals = readPrincipals()
    chatId = update.effective_chat.id
    user = allTeleBotUsersChatID[chatId]

    infoButtons = [[KeyboardButton(i)] for i in allInlinebuttons[1::]]

    embassyButtons = [[KeyboardButton(emb)] for emb in EMBInlineButtons]

    #see the principals
    if allButtonsInAfterStartMenue[0] in update.message.text:
        context.bot.send_message(text=pricesAndPrincipals, chat_id=chatId)

    #purchesing
    elif allButtonsInAfterStartMenue[1] in update.message.text:
        #I agree with the terms - next is to show ways of paymentE
        agreeButton = [[
            InlineKeyboardButton(allInlinebuttons[0],
                                 callback_data="accepted The terms")
        ]]

        context.bot.send_message(chat_id=chatId,
                                 text=pricesAndPrincipals,
                                 reply_markup=InlineKeyboardMarkup(
                                     agreeButton, resize_keyboard=True))

    #edit/add gmail or pass
    elif allButtonsInAfterStartMenue[2] in update.message.text:
        if checkPayment(chatId):

            attempt=1
            try:
                with open(f'Users/{user.username}-{chatId}/schedule_count.txt',
                          'r') as f:
                    attempt=int(f.read())
                if attempt==0:
                    context.bot.send_message(chat_id=chatId,
                                     text='ابتدا هزینه ۲۰۰ هزارتومان برای سرور را پرداخت کنید.')
            except:
                pass

            if attempt!=0:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='لطفا اطلاعات خود را ویرایش یا وارد کنید.',
                    reply_markup=ReplyKeyboardMarkup(infoButtons,
                                                        resize_keyboard=True))
        else:
            context.bot.send_message(chat_id=chatId,
                                     text='ابتدا هزینه ۲۰۰ هزارتومان برای سرور را پرداخت کنید.')

    elif allInlinebuttons[3] in update.message.text:

        context.bot.send_message(
            chat_id=chatId,
            text=
            'لطفا سفارت مقصد را انتخاب کنید.\n در صورتی که سفارت مورد نظر در لیست نیست می توانید اطلاعات کاربری حساب سفارت خود (ایمیل و رمز عبور و ادرس سایت سفارت مورد نظر) را در قالب یک پیام برای پشتیبانی بفرستید.',
            reply_markup=ReplyKeyboardMarkup(embassyButtons,
                                             resize_keyboard=True))

    elif allInlinebuttons[5] in update.message.text:
        msgLogin = ''
        
        if loginCheck(chatId):
            msgLogin = f'''شما با اطلاعات ورودی: \nایمیل: {user.email}\nرمزعبور: {user.password}\nسفارت: {user.location}\nبا موفقیت وارد شدید.'''

        else:
            msgLogin = f'''اطلاعات ورودی اشتباه است. لطفا دوباره تلاش کنید. \nایمیل: {user.email}\nرمزعبور: {user.password}\nسفارت: {user.location}'''

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=msgLogin,
                                 reply_markup=showMenueButtons())

    elif allInlinebuttons[6] in update.message.text:

        context.bot.send_message(chat_id=chatId,
                                 text='وارد منو اصلی شدید.',
                                 reply_markup=showMenueButtons())

    #location duabi
    elif EMBInlineButtons[0] in update.message.text:

        user.location = 'Dubai'
        updateInfo()
        context.bot.send_message(
            chat_id=chatId,
            text=f'سفارت انتخاب شده {user.location} است.',
            reply_markup=showMenueButtons())

    #location abu dhabi 
    elif EMBInlineButtons[1] in update.message.text:

        user.location = 'Abu Dhabi'
        updateInfo()
        context.bot.send_message(
            chat_id=chatId,
            text=f'سفارت انتخاب شده {user.location} است.',
            reply_markup=showMenueButtons())






RECIVEMAIL = 5


def askForMail(update: Update, context: CallbackContext):
    global allInlinebuttons

    if allInlinebuttons[1] in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='لطفا ایمیل خود را ارسال کنید.')
    return RECIVEMAIL


def getEmail(update: Update, context: CallbackContext):
    gmail = update.message.text
    allTeleBotUsersChatID[update.effective_chat.id].email = gmail

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'ایمیل با موفقیت دریافت شد:\n{allTeleBotUsersChatID[update.effective_chat.id].email}',
        reply_markup=showMenueButtons())

    updateInfo()

    return ConversationHandler.END


def errorEmail(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='لطفا دوباره امتحان کنید.',
                             reply_markup=showMenueButtons())
    return ConversationHandler.END


RECIVEDMSG = 4


def chatMsg(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='پیام خود را بنویسید.',
                             reply_markup=ForceReply(resize_keyboard=True))
    return RECIVEDMSG


def sentMsg(update: Update, context: CallbackContext):
    msg = update.message.text
    #print(msg,'send')
    insertMsgtoChatHelpTxt(update.effective_chat.id, msg)
    insertToToDoList(update.effective_chat.id, msg)
    #forward to admin
    '''msg=f'username {update.effective_chat.username} - chatID {update.effective_chat.id} needs help:\n {msg}'
    sendAdminMsg(msg ,context)'''
    forward_to_chat(update, context, message='help')

    text = 'پیام شما دریافت شد. در اولین فرصت پاسخ داده می شود.'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=showMenueButtons())

    return ConversationHandler.END



def errorHelp(update: Update, context: CallbackContext):
    text='لطفا دوباره امتحان کنید.'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=showMenueButtons())
    return ConversationHandler.END

RECIVEPASSWORD = 3


def askForPassword(update: Update, context: CallbackContext):
    global allInlinebuttons

    if allInlinebuttons[2] in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='لطفا رمز عبور خود را ارسال کنید.')
    return RECIVEPASSWORD


def getPassword(update: Update, context: CallbackContext):
    password = update.message.text
    allTeleBotUsersChatID[update.effective_chat.id].password = password
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'رمز عبور با موفقیت دریافت شد :\n{allTeleBotUsersChatID[update.effective_chat.id].password}',
        reply_markup=showMenueButtons())

    updateInfo()
    return ConversationHandler.END


def errorPassword(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='لطفا دوباره امتحان کنید.',
                             reply_markup=showMenueButtons())
    return ConversationHandler.END


RECIVEDESIREDSDATE = 2
RECIVEDESIREDEDATE = 1


def askForDesiredDates(update: Update, context: CallbackContext):
    global allInlinebuttons

    if allInlinebuttons[4] in update.message.text:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            'لطفا بازه زمانی دلخواه خود را به فرمت سال-ماه-روز میلادی ارسال کنید. \n مثلا برای تاریخ ۱۲ ماه می سال ۲۰۲۴: \n 2024-06-12 بنویسید.'
        )

        time.sleep(1)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='حال مطابق فرمت گفته شده ابتدای تاریخ مورد نظر را وارد کنید. \n توجه کنید وقت سفارت ب فاصله حداقل دو هفته بعد از تاریخ انتخاب شده رزرو می شود تا زمان کافی برای رسیدن به مصاحبه وجود داشته باشد.')

    return RECIVEDESIREDSDATE


def errorDate(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='لطفا دوباره امتحان کنید.',
                             reply_markup=showMenueButtons())
    return ConversationHandler.END


def getStartOfDesiredDate(update: Update, context: CallbackContext):
    global allTeleBotUsersChatID
    startDate = update.message.text
    if check_date_format(startDate):

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'تاریخ شروع ,با موفقیت دریافت شد.\n {startDate}',
            reply_markup=showMenueButtons())
    else:
        errorDate(update, context)
        return ConversationHandler.END

    time.sleep(1)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='حال مطابق فرمت گفته شده پایان تاریخ مورد نظر را وارد کنید.')
    timeTemp = datetime.strftime( datetime.strptime(startDate,'%Y-%m-%d'),  '%Y-%m-%d')
   
    allTeleBotUsersChatID[update.effective_chat.id].desired_date[0] = timeTemp
    updateInfo()
    return RECIVEDESIREDEDATE


def getEndOfDesiredDate(update: Update, context: CallbackContext):
    endDate = update.message.text
    user = allTeleBotUsersChatID[update.effective_chat.id]
    user.desired_date[1] = endDate
    print(endDate)
    ED = datetime.strptime(str(user.desired_date[1]), '%Y-%m-%d').date()
    SD = datetime.strptime(str(user.desired_date[0]), '%Y-%m-%d').date()
    print(ED, SD)

    if check_date_format(endDate):
        if ED > SD:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=
                f'تاریخ پایان بازه مورد نظر ,با موفقیت دریافت شد.\n {endDate}',
                reply_markup=showMenueButtons())
            user.desired_num_months = get_desired_num_months(user.desired_date)

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=
                f'تاریخ پایانی بازه موزد نظر بایستی بعد از شروع بازه باشد. \n  لطفا دوباره امتحان',
                reply_markup=showMenueButtons())
            return ConversationHandler.END
    else:
        errorDate(update, context)
        return ConversationHandler.END

    updateInfo()
    return ConversationHandler.END


def claimOfPaymen(username, chat_id):
    global allTeleBotUsersChatID
    user = allTeleBotUsersChatID[chat_id]

    #send message to admin

    with open('TODO/ToCheckPayment.txt', 'a+') as file:
        file.write(f'{username} {chat_id} \n')


#RECIVEDPHOTO=0
'''
def askForPhoto(update: Update, context: CallbackContext):
    print('ge')
    context.bot.send_message(chat_id=update.effective_chat.id,
         text='لطفا عکس پرداخت را بفرستید.')
    return RECIVEDPHOTO


def downloader(update: Update, context: CallbackContext):
    path = f'Users/{update.effective_chat.username}-{update.effective_chat.id}'

    (context.bot.getFile(update.message.photo[-1].file_id)).download(
        f'{path}/{update.effective_chat.username}-{update.effective_chat.id}.png')

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='عکس دریافت شد. لطفا منتظر تایید آن بمانید. با تشکر',reply_markup= showMenueButtons())

    claimOfPaymen(update.effective_chat.username, update.effective_chat.id)
    return ConversationHandler.END


def errorPhoto(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='لطفا دوباره امتحان کنید.', reply_markup= showMenueButtons())
    return ConversationHandler.END
    '''


def reply(update: Update, context: CallbackContext):
    user_id = None
    global allTeleBotUsersChatID
    '''if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )'''

    if 'photo' in update.message.reply_to_message.text:

        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[1])
        except ValueError:
            user_id = None
        username = allTeleBotUsersChatID[user_id].username
        if user_id:
            if '0' == update.message.text:
                setLastPaymentStatus(user_id, False)
                context.bot.send_message(
                    chat_id=user_id,
                    text='عکس پرداخت شما تایید نشد. لطفا دوباره امتحان کنید.')

                sendAdminMsg(f'You declined payment of {user_id}--{username}',
                             context)

                with open(f'Users/{username}-{user_id}/schedule_count.txt',
                          'w') as f:
                    f.write('0')

            elif '1' == update.message.text:
                # send msg to user and confirm
                setLastPaymentStatus(user_id, True)
                context.bot.send_message(
                    chat_id=user_id,
                    text=
                    'پرداخت با موفقیت تایید شد.'
                )
                sendAdminMsg(f'You approved payment of {user_id}--{username}',
                             context)

                with open(f'Users/{username}-{user_id}/schedule_count.txt',
                          'w') as f:
                    f.write('1')

            else:
                context.bot.send_message(chat_id=adminChatID(),
                                         text='WRONG_REPLY')
        else:
            context.bot.send_message(chat_id=adminChatID(),
                                     text='WRONG_REPLY PHOTO')
    elif 'help' in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[1])
        except ValueError:
            user_id = None

        if user_id:
            context.bot.copy_message(message_id=update.message.message_id,
                                     chat_id=user_id,
                                     from_chat_id=update.message.chat_id)
        else:
            context.bot.send_message(chat_id=adminChatID(), text='WRONG_REPLY')


#if tehranTime().minute==0 and tehranTime().hour==0:

#exec(open('test.py').read())

#asyncio.run(afterPayment())
#MessageHandler(~Filters.regex('.*@gmail.com$')
dispatcher.add_handler(CommandHandler("start", showMenue))



hlep_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex(allButtonsInAfterStartMenue[3]), chatMsg)
    ],
    fallbacks=[MessageHandler(~Filters.text,errorHelp)
        ],
    states={RECIVEDMSG: [MessageHandler(Filters.text, sentMsg)],
    },
    run_async=True)

dispatcher.add_handler(hlep_conv_handler)


dispatcher.add_handler(
    MessageHandler(Filters.chat(adminChatID()) & Filters.reply, reply))

#dispatcher.add_handler(MessageHandler(Filters.regex('.*@*.com$'), getEmail))

pass_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex(allInlinebuttons[2]), askForPassword)
    ],
    fallbacks=[MessageHandler(Filters.text, errorPassword)],
    states={RECIVEPASSWORD: [MessageHandler(Filters.text, getPassword)]},
    run_async=True)

dispatcher.add_handler(pass_conv_handler)

dates_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex(allInlinebuttons[4]), askForDesiredDates)
    ],
    fallbacks=[
        MessageHandler(
            Filters.text
            and ~Filters.regex('20[2-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
            errorDate)
    ],
    states={
        RECIVEDESIREDSDATE: [
            MessageHandler(
                Filters.text
                and Filters.regex('20[2-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
                getStartOfDesiredDate)
        ],
        RECIVEDESIREDEDATE: [
            MessageHandler(
                Filters.text
                and Filters.regex('20[2-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
                getEndOfDesiredDate)
        ]
    },
    run_async=True)

dispatcher.add_handler(dates_conv_handler)

mail_conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex(allInlinebuttons[1]), askForMail)
    ],
    fallbacks=[
        MessageHandler(Filters.text and ~Filters.regex('.*@*.com$'),
                       errorEmail)
    ],
    states={
        RECIVEMAIL: [MessageHandler(Filters.regex('.*@*.com$'), getEmail)],
    },
    run_async=True)

dispatcher.add_handler(mail_conv_handler)

dispatcher.add_handler(CallbackQueryHandler(agreeWithTermsButton))
'''photo_conv_handler = ConversationHandler(
    entry_points=[        MessageHandler(Filters.regex(sendPhotoText), askForPhoto)],
    fallbacks=[
        MessageHandler(~Filters.photo, errorPhoto)
    ],

    states={
        RECIVEDPHOTO: [MessageHandler(Filters.photo, downloader)]
    },
    run_async=True
)

dispatcher.add_handler(photo_conv_handler)'''
dispatcher.add_handler(MessageHandler(Filters.photo, downloader))

dispatcher.add_handler(
    MessageHandler(
        Filters.text and ~Filters.regex(allInlinebuttons[1]) and
        ~Filters.regex('.*@*.com$') and
        ~Filters.regex(allButtonsInAfterStartMenue[3]),
        chooseMenue))

updater.start_polling()
#dispatcher.add_handler(CallbackQueryHandler(afterPaymentMenue))
'''statuCheck = updater.job_queue
job_daily = statuCheck.run_daily(updatePaymentStatus(), days=(0, 1, 2, 3, 4, 5, 6),time=datetime.time(hour=11, minute=21, second=00,tzinfo=pytz.timezone('Asia/Tehran') ))
'''
#pytz.timezone
'''if tehranTime().hour==11 :
  asyncio.run(updatePaymentStatus())'''

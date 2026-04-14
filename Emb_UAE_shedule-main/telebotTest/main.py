from mainExtention import *
'''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
'''
#url=Users/{update.effective_chat.username}-{update.effective_chat.id}
updater = Updater(token=token)
dispatcher = updater.dispatcher


def updateInfo():
    global allTeleBotUsersChatID,usernamesChatId
    paths=['Users/allTeleBotUsersChatIdUser.pkl','Users/allusernamesChatId.pkl']
    dicts=[allTeleBotUsersChatID,usernamesChatId]
    
    for i, path in enumerate(paths):
        with open(path,'wb') as file:
            pickle.dump(dicts[i], file)
    
def validatePayemntByAdmin():
    pass

def newPayment(user):
    paymentsNofitications=user.paymentsNotifications
    numberOfweeks = len(paymentsNofitications.keys())
  
    if numberOfweeks>0:
        #payed? notification? date
        if paymentsNofitications[numberOfweeks][0]:
            paymentsNofitications[numberOfweeks+1]=[False,False,timeNow()]

def addTeleBotUser(chat_id,username):
    newUser=TelegaBotUser(chat_id,username)
    checkPath(username,chat_id)
    allTeleBotUsersChatID[chat_id]=newUser
    usernamesChatId[username]=chat_id
    #wirte to files
    updateInfo()

def showMenueButtons(): 
    global allButtonsInAfterStartMenue
    buttons = [[KeyboardButton(allButtonsInAfterStartMenue[i])]
         for i in range(5)]
    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    return reply_markup

def showMenue(update: Update, context: CallbackContext):
  global allButtonsInAfterStartMenue

  addTeleBotUser(update.effective_chat.id, update.effective_chat.username)

  #print(update.effective_chat.username)
  #print(update.message.text)
  text= "برای مطلع شدن از چگونگی گرفتن وقت سفارت به شرایط و هزینه ها مراجعه کنید."

  context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=text,
      reply_markup=showMenueButtons())



def checkLogin(chatId):
    #if True make a user in main and work for a week //TODO
    #now add email and password
    updateInfo()
    #check user payed for it rather that sent the right command
    print('check login')
    pass


def downloader(update: Update, context: CallbackContext):
    #insert the week to the path too
    path = f'Users/{update.effective_chat.username}-{update.effective_chat.id}'
    
    (context.bot.getFile(update.message.photo[-1].file_id)).download(
        f'{path}/{update.effective_chat.username}-{update.effective_chat.id}.png')
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='عکس دریافت شد. لطفا منتظر تایید آن بمانید. با تشکر',reply_markup= showMenueButtons())
    
    claimOfPaymen(update.effective_chat.username, update.effective_chat.id)
    
def agreeWithTermsButton(update: Update, context: CallbackContext):
    #now sending info about how to purches
    global allButtonsInAfterStartMenue
    query = update.callback_query.data
    update.callback_query.answer()

    chat_id=update.effective_chat.id

    
    if 'accepted The terms' in query:
        #send info about payment


        context.bot.send_photo(chat_id=chat_id,
                               photo=open('teter.png', 'rb'),
                               caption=" QRcode" + "\nERC20 شبکه")
        
        context.bot.send_message(chat_id=chat_id,
             text=getHasStrTxt())
        
        context.bot.send_message(chat_id=chat_id,
             text='لطفا عکس پرداخت را بفرستید.')
    #location!!!!!!!!!!!!!!!!!!!!!!!    

            
     
'''    
def checkClaimOfPayment(username, chat_id):
    with open(f'Users/{username}-{chat_id}/claim.txt', 'r') as file:
        file.readline()
        flag = file.readline().split(' ')[1]

    if flag == 'True':
        print(f'payed {username} {chat_id}')
        return True
    else:
        print(f'has not payed yet {username} {chat_id}')
        return False'''



def notifyUser(username, chat_id):
    #admin notify this this notifyes user reply
    pass


def chooseMenue(update: Update, context: CallbackContext):
    global allButtonsInAfterStartMenue, allInlinebuttons
    
    pricesAndPrincipals = readPrincipals()
    chatId=update.effective_chat.id

    #see the principals
    if allButtonsInAfterStartMenue[0] in update.message.text:
        context.bot.send_message(text=pricesAndPrincipals,
                                 chat_id=chatId)

    #purchesing
    elif allButtonsInAfterStartMenue[1] in update.message.text:
        #I agree with the terms - next is to show ways of paymentE
        agreeButton = [[
            InlineKeyboardButton(allInlinebuttons[0],
                                 callback_data="accepted The terms")
        ]]

        context.bot.send_message(chat_id= chatId,
                                 text=pricesAndPrincipals,
                                 reply_markup=InlineKeyboardMarkup(
                                     agreeButton, resize_keyboard=True))

    #calender
    elif allButtonsInAfterStartMenue[2] in update.message.text:
        #show calender from main
        pass
        
    #edit/add gmail or pass
    elif allButtonsInAfterStartMenue[3] in update.message.text:
        if checkPayment(chatId):
            infoButtons =  [[KeyboardButton(allInlinebuttons[i])] for i in range(1,4)]
        
            context.bot.send_message(chat_id=update.effective_chat.id,
                 text='لطفا اطلاعات خود را ویرایش یا وارد کنید.',
                 reply_markup=ReplyKeyboardMarkup(
                     infoButtons, resize_keyboard=True))
        else:
            context.bot.send_message(chat_id= chatId,
                 text='ابتدا هزینه را پرداخت کنید.')

    elif allInlinebuttons[3] in update.message.text:
                
        context.bot.send_message(chat_id= chatId,
             text='وارد منو اصلی شدید.', reply_markup=showMenueButtons())
        

async def afterPayment():
    #admin gives a signal so then the status will become true
    
    '''    with open('TODO/ToCheckPayment.txt', 'r') as file:
            try:
                lines = file.readlines()
                username, chatId, _ = lines.pop(0).split(' ')
    
            except:
                return
                
        if checkClaimOfPayment:
            if  notifyUser(username, chatId) == True:
                message = 'شما با موفقیت پرداخت کردید'
                updater.bot.send_message(chat_id=chatId,text=message)
                
                with open('TODO/ToCheckPayment.txt', 'w') as file:
                    for line in lines:
                        file.write(line)'''


RECIVEMAIL=3

def askForMail(update: Update, context: CallbackContext):
    global allInlinebuttons
    
    if allInlinebuttons[1] in update.message.text:
      context.bot.send_message(chat_id=update.effective_chat.id,
         text='لطفا ایمیل خود را ارسال کنید.') 
    return RECIVEMAIL
    
def getEmail(update: Update, context: CallbackContext):
    gmail = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ایمیل با موفقیت دریافت شد.', reply_markup= showMenueButtons())

    allTeleBotUsersChatID[update.effective_chat.id].email=gmail
    checkLogin(update.effective_chat.id)

    return ConversationHandler.END

def errorEmail(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='لطفا دوباره امتحان کنید.', reply_markup= showMenueButtons())
    return ConversationHandler.END



RECIVEDMSG=2

def chatMsg(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id= update.effective_chat.id,
         text='پیام خود را بنویسید.', reply_markup=ForceReply(resize_keyboard=True))
    return RECIVEDMSG


def sentMsg(update: Update, context: CallbackContext):
    msg=update.message.text
    insertMsgtoChatHelpTxt(update.effective_chat.id,msg)
    insertToToDoList(update.effective_chat.id,msg)
    #forward to admin
    msg=f'username {update.effective_chat.username} - chatID {update.effective_chat.id} needs help:\n {msg}'
    sendAdminMsg(msg ,context)
    text='پیام شما دریافت شد. در اولین فرصت پاسخ داده می شود.'
    context.bot.send_message(chat_id= update.effective_chat.id,
         text=text, reply_markup=showMenueButtons())
    
    return ConversationHandler.END


RECIVEPASSWORD=1


def askForPassword(update: Update, context: CallbackContext):
    global allInlinebuttons

    if allInlinebuttons[2] in update.message.text:
      context.bot.send_message(chat_id=update.effective_chat.id,
         text='لطفا رمز عبور خود را ارسال کنید.') 
    return RECIVEPASSWORD

def getPassword(update: Update, context: CallbackContext):
    password = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='رمز عبور با موفقیت دریافت شد.', reply_markup= showMenueButtons())

    allTeleBotUsersChatID[update.effective_chat.id].password=password
    checkLogin(update.effective_chat.id)
    return ConversationHandler.END



def claimOfPaymen(username, chat_id):
    global allTeleBotUsersChatID
    user=allTeleBotUsersChatID[chat_id]
    newPayment(user)
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
#asyncio.run(afterPayment())
#MessageHandler(~Filters.regex('.*@gmail.com$')
dispatcher.add_handler(CommandHandler("start", showMenue))
#dispatcher.add_handler(MessageHandler(Filters.regex('.*@*.com$'), getEmail))
pass_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(allInlinebuttons[2]), askForPassword)],
    fallbacks=[],

    states={
        RECIVEPASSWORD: [MessageHandler(Filters.text, getPassword)]
    },
    run_async=True
)

dispatcher.add_handler(pass_conv_handler)

mail_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(allInlinebuttons[1]), askForMail)],
    fallbacks= [MessageHandler(Filters.text and ~Filters.regex('.*@*.com$') , errorEmail)
    ],

    states={   

        RECIVEMAIL: [MessageHandler(Filters.regex('.*@*.com$'), getEmail)],
    },
    run_async=True
)

dispatcher.add_handler(mail_conv_handler)


hlep_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(allButtonsInAfterStartMenue[4]), chatMsg)],
    fallbacks=[],

    states={
        RECIVEDMSG: [MessageHandler(Filters.text, sentMsg)]
    },
    run_async=True
)

dispatcher.add_handler(hlep_conv_handler)
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

dispatcher.add_handler(MessageHandler(
    Filters.text and
    ~Filters.regex(allInlinebuttons[1]) and
    #~Filters.regex('.*@*.com$') and
    ~Filters.regex(allButtonsInAfterStartMenue[4]), chooseMenue
                                     ))

#dispatcher.add_handler(CallbackQueryHandler(afterPaymentMenue))

updater.start_polling()

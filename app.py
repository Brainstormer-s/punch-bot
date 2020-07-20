from urllib.request import urlopen
from datetime import datetime 
from bs4 import BeautifulSoup
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


dateNow = datetime.now().strftime("%Y-%m-%d")
html = urlopen(f'https://www.boxofficemojo.com/date/{dateNow}/weekly/')
 
res = BeautifulSoup(html.read(),"html5lib")
MTitle = res.find("h1", {"class": "mojo-gutter"})
Titles = res.findAll("h3", {"class": "a-size-base"})  

ranks = res.findAll("td", {"class": "mojo-field-type-rank"})  
mmtitle = MTitle.getText()
boxf = ""
n=0
for Title in Titles:
    n += 1
    boxf += f"{n} {Title.getText()} \n"
    
    if n > 9: 
        break

HOME , WAY = range(2)

def home (update, context):
    reply_keyboard = [['/Box_office', '/Other']]
    update.message.reply_text(F'What can i do for you ',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return WAY

def box_Office (update, context):
    reply_keyboard = [['/Back']]
    update.message.reply_text(F'{mmtitle} \n \n {boxf}',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return HOME

def main():
    updater = Updater("YOUR BOT TOKEN FROM BOTFATHER", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', home)],

        states={
            WAY: [CommandHandler('Box_office', box_Office)],
            HOME: [CommandHandler('Back', home)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == '__main__':
    main()








      




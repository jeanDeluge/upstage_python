import os
import telegram
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
async def main():
    



    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    bot = telegram.Bot(TOKEN)

    # ID = os.getenv("ID")
    # chat_id=await bot.get_updates(limit=1).update_id
    # print(chat_id)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application = ApplicationBuilder().token('TOKEN').build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()


    # 최근 메시지를 업데이트할거다
    # updater=Update(TOKEN).message
    # test=updater.message.test
    # print(updater)
    # dispatcher=Updater.dispatcher
    # dispatcher.add_handler(MessageHandler(filters.text))



    # chat_id=await bot.getUpdates()[-1].message.chat.id
    # await bot.send_message(chat_id, text='hi')
    # new_file=await bot.getFile()
    # for u in updates:
    #     print(u.message)


    # await bot.send_message(chat_id=ID, text="명령은 한번에 하나만 해주세요.\n 1) 뉴스 보내줘\n 2) 뉴스 요약해줘\n 3) 원하는 도시의 날씨 알려줘 \n 4) 원하는 도시의 현지시각 알려줘\n")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
import os
from pyrogram import Client,filters,emoji
from pyrogram.types import ChatPermissions
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,CallbackQuery



bot = Client("monitoring server bot"
             ,api_id=29365133,api_hash="722d0eb612a789286c0ed9966c473ddf"
                ,bot_token="5873524421:AAHWQzlbGhhUdkiwhfanf9dK0SfC_NzYQQ8")




start_message = "heya , ali khar kosde"
start_message_button=[
    [InlineKeyboardButton('channel' , url="www.codeil.ir"),
     InlineKeyboardButton('channel' , url="www.codeil.ir")
     ],
    [InlineKeyboardButton('channel' , url="www.codeil.ir")]
]


@bot.on_message(filters.command('start') & filters.private)
def command1(bot,message):
    text = start_message
    reply_markup = InlineKeyboardMarkup(start_message_button)
    message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )




print("bot started")
bot.run()

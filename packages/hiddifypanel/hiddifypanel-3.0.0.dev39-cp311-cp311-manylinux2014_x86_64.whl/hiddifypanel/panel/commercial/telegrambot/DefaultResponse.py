from . import bot


@bot.message_handler(func=lambda message: True)
def not_handled(message):
    bot.reply_to(message, "We can not understand your request")


@bot.callback_query_handler(func=lambda call: True)
def update_usage_callback(call):  # <- passes a CallbackQuery type object to your function
    bot.answer_callback_query(call.id, "Incorrect callback", cache_time=1)
#واقعا برای 5 دلار میخوای کرک میکنی؟ حاجی ارزش وقت خودت بیشتره
#Email hiddify@gmail.com for free permium version. Do not crack this cheap product

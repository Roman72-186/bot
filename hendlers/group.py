# from string import punctuation

# from aiogram import F, types, Router

# user_group = Router()

# restricted_words = {
#     'сука',
#     'кабан',
#     'корова'
# }

# def clean_text(text: str):
#     return text.translate(str.maketrans('', '', punctuation))

# def reply_text(text: str):
#     return text.translate(str.maketrans('', '', punctuation))

# @user_group.edited_message()
# @user_group.message()
# async def start_cmd(message: types.Message):
#     if restricted_words.intersection(clean_text(message.text.lower()).split()):
#         await message.reply(f'{message.from_user.first_name}, соблюдайте порядок!')
#         await message.delete()
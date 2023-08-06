from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 

def memekontol():
    return InlineKeyboardMarkup([[InlineKeyboardButton("CHANNEL", url=f"https://t.me/RendyProjects")]])

async def randydevhack(client, message, chat_id, message_id):
    await client.copy_message(message.chat.id, from_chat_id=chat_id, message_id=message_id, caption=None, reply_to_message_id=message.id)

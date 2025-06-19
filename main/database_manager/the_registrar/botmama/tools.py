from telethon import TelegramClient, events
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()
api_id = os.environ["BMAMA_ID"]
api_hash = os.environ["BMAMA_HASH"]
session_name = 'some'



async def send_message(message):
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    ent = await client.get_entity(entity="BotFather")
    await client.send_message(ent,message)
    await asyncio.sleep(3)
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def receive_message():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    ent = await client.get_entity(entity="BotFather")
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def run(func:str, msg:str):
    if func == "send_message":
        return await send_message(msg)
    else:
        return await receive_message()
    
run.__doc__ = """
Runs async functions and returns the message

Args:
func (str): Parameter choice can be either `send_message` or `receive_message`
msg(str): the message to parse if func=send_message, if receiving just return it as ''

Returns:
The response of the sender
"""
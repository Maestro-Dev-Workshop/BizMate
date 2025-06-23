from telethon import TelegramClient, events
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
SESSION_NAME = Path("sessions",str(os.environ["ROUTER_SESSION"]))
API_ID = os.environ["ROUTER_ID"]
API_HASH = os.environ["ROUTER_HASH"]


async def send_message(message, contact):
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    ent = await client.get_entity(entity=contact)
    await client.send_message(ent,message)
    await asyncio.sleep(3)
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def receive_message(contact):
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    ent = await client.get_entity(entity=contact)
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def run(func:str, msg:str, contact:str):
    if func == "send_message":
        return await send_message(msg, contact)
    else:
        return await receive_message(contact)
    
run.__doc__ = """
Runs async functions and returns the message

Args:

func (str): Parameter choice can be either `send_message` or `receive_message`
msg(str): the message to parse if func=send_message, if receiving just return it as ''
contact(str): Name of the contact


Returns:
The response of the sender
"""

asyncio.run(run("send_message","wewfew","nolimitsxl"))
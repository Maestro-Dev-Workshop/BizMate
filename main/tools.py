from database_manager.tools import *
from telethon import TelegramClient, events
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = os.environ["ROUTER_ID"]
API_HASH = os.environ["ROUTER_HASH"]


def get_business_details(
        username: str
):
    """
    Specialized Bizmate Agent Tool.
    Get details of a business.

    Args:
        username (str): the telegram username of the business.
    Returns:
        A dictionary containing details of the business, with keys: id, username, name, age, gender, contact_details.
    """

    cols = ["id","username", "name", "business_name"]
    result = get_rows_with_exact_column_values(
        "business", 
        ["username"], 
        [username], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        if result:
            return {cols[i]: result[0][i] for i in range(len(cols))}
        else:
            return "business record not found"

def log(
    id :int
):
    """
    Once called, it logs the business
    Args:

    id(str):business id
    
    Returns whether it was successful or it failed
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return insert("log_history","(business_id, login_time)",(id,dt),"%s, %s")

def get_recent_orders(id):
    cursor.execute("SELECT MAX(login_time) FROM log_history WHERE business_id=%s",(id,))
    last_login = cursor.fetchone()
    last_login = last_login[0]
    cursor.execute("SELECT * FROM customer_order WHERE business_id=%s and TIMESTAMPDIFF(MINUTE, date_ordered, %s) <= 30", (id,last_login))
    return cursor.fetchall()

async def send_message(message, session_name, contact):
    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.start()
    ent = await client.get_entity(entity=contact)
    await client.send_message(ent,message)
    await asyncio.sleep(3)
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def receive_message(contact,session_name):
    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.start()
    ent = await client.get_entity(entity=contact)
    message = [msg.text async for msg in client.iter_messages(ent, limit=1)]
    await client.disconnect()
    return message

async def run(func:str, session_name:str, msg:str, contact:str):
    if func == "send_message":
        return await send_message(msg, session_name, contact)
    else:
        return await receive_message(contact, session_name)
    
run.__doc__ = """
Runs async functions and returns the message

Args:

func (str): Parameter choice can be either `send_message` or `receive_message`
session_name(str) : Name of the Session
msg(str): the message to parse if func=send_message, if receiving just return it as ''
contact(str): Name of the contact


Returns:
The response of the sender
"""
get_business_details.__doc__ = """
Gets business details

Args:
username(str): Telegram username

Returns :
Whether it exists
"""
log.__doc__ = """
Logs Business details

Args:
id: The business id

Returns
Whether operation was successful

"""
get_recent_orders.__doc__ = """
Get the recent order made 
"""


send_message()
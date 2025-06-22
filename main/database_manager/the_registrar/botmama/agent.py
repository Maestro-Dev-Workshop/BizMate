# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from google.adk.agents import Agent
from utils.tg_utils import run

bot_mama = Agent(
    name="bot_mama",
    description="Creates Bots for Businesses",
    model="gemini-2.0-flash",
    instruction="""You are bot mother, the creator of telegram bots for Businesses.
    You are going to receive the name of the business.
    Proceed to create the bot, by chatting with BotFather using the tool provided.
    If BotFather needs an information, provide the information to BotFather, do not include any other text and you must provide it without asking the user.

    DO NOT ask the user for any information from the user, you are to use the business name provided to you.

    The name of the bot should be the business name
    The username should also be the business name, however it should be formatted in the following way:
        - letter must be in small caps
        - any spaces between words should be replaced with underscores
        - if the username already exists, add 3 digits randomly selected

    Do not send any message to BotFather, only if you receive a message that the bot has been created successfully.

    # Scenario:
    - If you're unable to create the bot, return `Your bot will be created later`.
    
    Once you're done with bot creation , Message the created bot with `/start` (use the formatted username as the contact parameter).
    Output only the username, link to the bot, and the token, and nothing else.
    """,
    tools=[run]
)


from google.adk.agents import Agent
from google.adk.tools import agent_tool
from .botmama.agent import bot_mama
from .tools import *

the_registrar = Agent(
    name="the_registrar",
    model="gemini-2.0-flash",
    description="Agent responsible for registering business basic information into the database.",
    instruction=f"""
    You are the business registrar. When executing a task, do not ask for permission; simply follow the instructions and return only the final result (do not explain your thought process). Your tasks include:
    - Registering a user's business basic information in the database.
    - Deleting a business from the database.
    - Verifying a business in the database.

    Table business description:
    {describe_table("business")}

    An account having active=0 means it has been deleted, so make sure you work with active account by filtering it

    ### Registering a Business ###;
    To successfully register a business, ensure you have the following details:
        1. User name
        2  Name
        3. Business name
        4. Brief description of the business
        5. User's contact details (email only)
        6. User's physical address
        7. User's date of birth (YYYY-MM-DD) to confirm age above 18
    
    If you receive a context with business information, extract the above details. If any are missing, inform the user which details are needed.

    After gathering all required information and they are all verified:
        - Create Customer Agent Bot for the business using bot_mama tool, provide the tool with the Business Name only, do not request for bot username or link from the user.
        - If the bot creation is successful, you will receive the bot username, link, and token.
    
    After bot creation:
        - proceed to add all the details you've collected using add_business tool, if bot creation failed, just use '' as the value (applicable for only bot parameters) and inform the user that, Due to limits the bot will be created later.

    If registration was successful, return the following, **business_name**(**business_id**) has been successful, you customers can buy your products using the bot **bot_link**. Do not add bot link if the bot creation failed.

    ### Deleting a Business ###
    Obtain the business name, verify its existence, then use the delete_business tool.

    ### Updating a Business ###
    Obtain the business name, verify its existence, collect the detail to update and value, then use the update_table tool, ensure you filter by active.
    """,
    tools=[add_business, verify_business, delete_business, update_table, agent_tool.AgentTool(bot_mama)]
)

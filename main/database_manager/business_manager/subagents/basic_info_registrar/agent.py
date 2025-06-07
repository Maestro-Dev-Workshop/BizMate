from google.adk.agents import Agent
from .tools import *

root_agent = Agent(
    name="Business_Registrar",
    model="gemini-2.0-flash",
    description="Agent capable of registering a business **basic_information** into the database",
    instruction="""
    You are the business registrar, responsible for registering a user's business basic information information into the database.
    You must collect the following information and they must be asked one at a time but in order:

    1. User name
    2. The Business Name
    3. Password
    3. A brief description of the business
    4. The contact details of the user (email only)
    5. The physical address of the user
    6. The User's date of birth, this is to make sure the user is above 18

    You may receive a context containing the business information, extract the details above from the context.
    If any of the details above were not found, inform the user they should provide information for those that were not found.

    While collecting the information required:
    - ensure the business name does not exist in database, using get_single_value tool. If it exist, inform the user the name exist and another name for the business should be provided.
    
    After receiving all the required information:
    - Show the users all the information you collected for confirmation
    - If the information was confirmed, add it to the database
    """,
    tools=[add_business, get_single_value]
)

# Issues
# business name should be formatted - all low caps, replace left space and  right space, replace space with _
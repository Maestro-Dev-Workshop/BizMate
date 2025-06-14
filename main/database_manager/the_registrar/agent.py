from google.adk.agents import Agent
from .tools import *

the_registrar = Agent(
    name="the_registrar",
    model="gemini-2.0-flash",
    description="Agent capable of registering a business **basic_information** into the database",
    instruction="""
    You are the business registrar,  while executing a task, do not ask for permission from the user,follow the instruction given and return only the final result( do not explain your thought process) based on the task the user gave you, . These are your following tasks:
    - Registering a user's business basic information information into the database.
    - Deleting a Business in the database
    - Verifying a business in the database

     ### Registering a Business ###
        You must collect the following information and they must be asked all at once but in order:

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
            - ensure the business name does not exist in database, using verify_business tool. If it exists, inform the user it exist then prompt the user to provide another business name.
        
        After receiving all the required information:
        - Show the users all the information you collected for confirmation (do not show the formatted name and business name).
        - If the information was confirmed, add it to the database.

    ### Deleting a Business ###
        Ensure you have the name of the business, verify whether the business exist, then use the tool delete_business.

    ### Updating a Business ##
        Ensure you have the name of the business, verify whether the business exist, collect the detail and the new value, then use the tool update_table to update the business.
    """,
    tools=[add_business, verify_business,delete_business,update_table]
)

# verify_business("xl_and_co")
# Issues
# business name should be formatted - all low caps, replace left space and  right space, replace space with _
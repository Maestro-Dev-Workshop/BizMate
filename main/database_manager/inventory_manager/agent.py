# Add, Modify, Delete
# Inform users any product low in stock
# Updating the stock
from google.adk.agents import Agent
from .tools import *
 
inventory_agent = Agent(
    name="inventory_manager",
    model="gemini-2.0-flash",
    description="Responsible for managing inventory, tasked with adding, modifying, deleting and giving report on the inventory",
    instruction=f"""
    You are the inventory manager and you will be provided with the business_name, and id, along with the task to do, 
    These are tasks you are allowed to do:
    - Add to inventory
    - Update Inventory
    - Deleting an Item
    - Giving a report on the items in the inventory
    You'll be working with the product table. 
    here's the description:
        {describe_table("product")}

    ## Add to inventory ##
        Tell the user to provide you with the following information:
        - The list of items to add (to be formatted)
        - The brand of each item (to be formatted)
        - The threshold limits of each item by brand
        - The quantities of each item by brand
        - The sold price of each item by brand
        - The minimum selling price of each item by brand
        - The expiry_date (YYYY-MM-DD)for each item by brand
        - Other information for each item by brand

        If any of the details above were not found, inform the user they should provide information for those that were not found.

        While collecting the information required:
        - ensure the item with that brand does not exist in database for that business use get_single_value tool. If it exist, inform the user that the item exist
        - If the user does not specify a minimum selling price, put in the value of selling price
        - If the expiry_date was not specified, or it doesn't have, it should a default value of 2035-12-31
        
        After receiving all the required information:
        - determine the most appropriate categories for each items listed, for example Phones will have a category electronics, first check all the categories within the system
        - After the adding to the database

    ## Update Inventory ##
        To update an inventory, the following details are required:
            - What item along with the brand to update
            - What detail to update, e.g the brand
            - The new value
        Verify the item exist with the brand name,then, ensure the new value for the detail follows the requirement, then you can proceed to update

    ## Deleting an Item ##
        To delete an item, you must know what item with the brand you are to delete, verify, then delete it.
    
    ## Report on Inventory ##
        Before giving a report check if the user have items in the inventory, if there are no items, report that only, if items exist report the following:
        Give on report on  all the following, ensure you rephrase and structure the output in such a way that the user can easily understand it, do not ask the user for a choice:
            - Items below minimum threshold in quantity
            - Items that have expired
    
    """,
    tools=[get_rows_with_exact_column_values,update_table, delete_row, add_item, get_expired_goods, execute_query_in_str]
)
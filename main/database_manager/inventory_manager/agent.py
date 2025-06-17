# Add, Modify, Delete
# Inform users any product low in stock
# Updating the stock
from google.adk.agents import Agent
from .tools import *
 
inventory_agent = Agent(
    name="inventory_manager",
    model="gemini-2.0-flash",
    description="Manages inventory items and products.",
    instruction=f"""
    You are the inventory manager. You will receive the business_name, id, and a specific inventory-related task. Only perform tasks related to inventory management.
    You will interact with the product table, structured as follows:
        {describe_table("product")}

    You are a tool for an agent, so always provide a final response.

    ## Adding to Inventory ##
        Request these details from the agent:
        - List of items to add (formatted)
        - Brand for each item (formatted)
        - Threshold limits for each item by brand
        - Quantities for each item by brand
        - Selling price for each item by brand
        - Minimum selling price for each item by brand
        - Expiry date (YYYY-MM-DD) for each item by brand
        - Any additional information for each item by brand

        If any required information is missing, prompt the agent to provide it.

        When gathering information:
        - Use get_single_value to check if an item with the same brand exists for the business. Notify the agent if it does.
        - If minimum selling price is not given, set it equal to the selling price.
        - If expiry date is missing or not applicable, default to 2035-12-31.

        Once all information is collected:
        - Assign the most appropriate category to each item (e.g., Phones -> electronics), referencing existing categories.
        - Add the items to the database.

    ## Updating Inventory ##
        To update inventory, determine:
            - The item name and brand to update
            - The detail to update and its new value
        Confirm the item exists with the specified brand, validate the new value, then update using update_table (include business_id).

    ## Deleting an Item ##
        To delete an item, identify the item and brand, verify its existence, and delete it using delete_row (include business_id).

    ## Deleting all items ##
        - Do not ask for permission.
        - Use delete_row, filtering by business id.

    ## Inventory Report ##
        Before generating a report, check if inventory has any items. If empty, inform the agent to add items before a report can be generated.
        If items exist, provide a clear, structured report covering only the following listed below:
            - Items below their minimum quantity threshold
            - Items that have expired using get_expired_goods()

        Do not report on the items the user has
        Ensure the report is easy to understand and do not prompt the agent for further choices.

    ## Notes ##
        - Use view_items to list inventory items..
        - When inserting multiple rows, combine all rows into a single function call.
    """,
    tools=[
        get_rows_with_exact_column_values,
        view_items,
        update_table,
        delete_row,
        add_item,
        get_expired_goods,
        execute_query_in_str,
        get_minimum_threshold
    ]
)

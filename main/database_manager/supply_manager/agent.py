#-Add Supplier,Modify and Delete
# Inform users which products doesn't have a supplier yet
# Make a supply_order
# Track unfufilled orders
# Update orders to fufilled  by the request of the user
# Delegate the task of adding quantity to inventory by the inventory manager
from google.adk.agents import Agent
from .tools import *

supply_agent = Agent(
    name="supply_manager",
    model="gemini-2.0-flash",
    description="Handles all supplier-related information management.",
    instruction=f"""You are tasked with managing supplier information for a business. When given a task, execute it directly without asking for user permission or explaining your reasoning. Only return the final result.
    You can only tasks as long as it relates to supply management

You will interact with the 'supplier' and 'supplier_inventory' tables in a MySQL database.

## Basic Management ##
### Adding Supplier Information
Ask the user for the supplier details to add. Inform them that the following information is required:
- Supplier name
- Contact email
- Items supplied
- Brands of supplied items
- Cost price per brand
- Stock availability

After collecting the details:
- Use get_rows_with_exact_column_values to check if the item and brand exist in the product table.
- If not found, notify the user that the product is not in inventory.
- Use add_supplier_and_supplier_inv to add the supplier and their inventory.

To find items without suppliers, use get_no_suppliers.

### Updating Supplier Information
To update, request:
- Item name and brand
- Supplier name
- Field to update
- New value

Verify the item and brand exist, determine the correct table, and update accordingly.

### Deleting Supplier or Item
To delete an item, require item name, brand, and supplier info. Verify and delete.
To delete a supplier, require the name. First, remove their inventory from supplier_inventory, then delete from supplier.

## Reporting ##
Before reporting, check if suppliers exist. If none, state so. Otherwise, report:
- Items without suppliers
- Items out of stock from current suppliers (use execute_query)
If no results, state accordingly.

## Reference Table Descriptions ##
product table:
    {describe_table("product")}
supplier table:
    {describe_table("supplier")}
supplier_inventory table:
    {describe_table("supplier_inventory")}
business table:
    {describe_table("business")}
""",
    tools=[
        get_no_suppliers,
        add_supplier,
        add_supplier_and_suppier_inv,
        add_to_supplier_inv,
        get_supplier_id_by_mail,
        get_supplier_inv_id,
        execute_query,
        delete_row,
        get_single_value,
        update_table
    ]
)
# doesn't format well
# doesn't give a good report
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.supply_manager.tools import *

def get_supplier_id_by_name(business_name:int,
                name: str) -> int:
    """
    Returns supplier id

    Args:
        business_name (str): name of the business
        name(str): Name of the supplier
        
    Returns:
        the supplier id, returns -1 if not found
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    cursor.execute("""SELECT id,name, contact_details from supplier WHERE business_id=%s AND name=%s""",(business_id,name))
    supplier_id = cursor.fetchall()
    cursor.reset()
    if len(supplier_id) > 1:
        return supplier_id
    elif len(supplier_id) == 1:
        return supplier_id[0][0]
    else:
        return -1


def add_supply_order(
    item_name : str,
    item_brand : str,
    business_name : str,
    supplier_name : str,
    quantity : int,
    supplier_id : int = -1,
) -> str:
    """
    Add an order to supply_order

    Args:
        item_name(str) : Name of the item
        item_brand(str) : brand of the item
        business_name(str) : Name of the item
        supplier_name(str) : Name of the Supplier
        quantity(int) : Quantity of items to be supplied
        supplier_id(int) : ID of the supplier, use only if you have the ID
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    product_id = get_product_id(business_id,item_name,item_brand)
    if product_id == -1:
        return "Product Not Found"
    supplier_id = get_supplier_id_by_name(business_name,supplier_name) if supplier_id == -1 else supplier_id
    if isinstance(supplier_id,int):
        if supplier_id == -1:
            return "Supplier does not exist"
        query = """SELECT * FROM supplier_inventory WHERE product_id=%s AND supplier_id=%s"""
        query_2 = """SELECT * FROM supplier_inventory WHERE product_id=%s AND supplier_id=%s AND available=%s"""
        
        cursor.execute(query,(product_id,supplier_id))
        output = cursor.fetchall()
        if len(output) == 0:
            return """Supplier doesn't have such product"""
        
        cursor.execute(query_2,(product_id,supplier_id,0))
        output = cursor.fetchall()
        if len(output) == 1:
            return """Item not available in Supplier stock"""
        
        time_of_order = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        columns = "(product_id, business_id, supplier_id, quantity_ordered, date_ordered, fulfilled)"
        vals = (product_id,business_id,supplier_id,quantity,time_of_order,0)
        vals_fmt = ", ".join(["%s" for _ in range(len(vals))])
        return insert("supply_order", columns, vals, vals_fmt)
    else:
        return f"Multiple Suppliers Found {supplier_id}"
    
print(get_product_id(7,"vegetable_oil","king"))

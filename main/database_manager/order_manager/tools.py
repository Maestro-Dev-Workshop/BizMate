import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.supply_manager.tools import *

def get_supplier_id_by_name(business_id:str,
                name: str) -> int:
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
    business_id : str,
    supplier_contact_det : str,
    quantity : int,
    supplier_id : int = -1,
) -> str:
    
    product_id = get_product_id(business_id,item_name,item_brand)
    if product_id == -1:
        return "Product Not Found"
    supplier_id = get_supplier_id_by_mail(business_id,supplier_contact_det) 
    if isinstance(supplier_id,int):
        if supplier_id == -1:
            return "Supplier does not exist"
        query = """SELECT * FROM supplier_inventory WHERE product_id=%s AND supplier_id=%s AND active=1"""
        query_2 = """SELECT * FROM supplier_inventory WHERE product_id=%s AND supplier_id=%s AND available=%s  AND active=1"""
        
        cursor.execute(query,(product_id,supplier_id))
        output = cursor.fetchall()
        if len(output) == 0:
            return """Supplier doesn't have such product"""
        
        cursor.execute(query_2,(product_id,supplier_id,0))
        output = cursor.fetchall()
        if len(output) == 1:
            return """Item not available in Supplier stock"""
        
        time_of_order = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        columns = "(product_id, business_id, supplier_id, quantity_ordered, date_ordered, order_status)"
        vals = (product_id,business_id,supplier_id,quantity,time_of_order,0)
        vals_fmt = ", ".join(["%s" for _ in range(len(vals))])
        return insert("supply_order", columns, vals, vals_fmt)
    else:
        return f"Multiple Suppliers Found {supplier_id}"
    
def get_unfulfilled_supplier_order(
        business_id: str,
    ) -> str:
    
    cursor.execute("""SELECT 
        so.id AS order_id,
        b.business_name,
        p.item_name,
        s.name AS supplier_name,
        so.quantity_ordered,
        so.date_ordered
    FROM supply_order so
    JOIN business b ON so.business_id = %s
    JOIN product p ON so.product_id = p.id
    JOIN supplier s ON so.supplier_id = s.id
    WHERE so.order_status=%s;
    """, (business_id,"pending"))
    return f"""{cursor.fetchall()}"""

def get_unfulfilled_customer_orders(
        business_id: str,
    ) -> str:
    
    query = """
    SELECT 
        co.id AS order_id,
        c.name AS customer_name,
        c.contact_details AS customer_contact,
        p.id AS product_id,
        p.item_name AS product_name,
        p.category,
        p.brand,
        co.quantity_ordered,
        co.sold_price,
        co.date_ordered
    FROM customer_order co
    JOIN customer c ON co.customer_id = c.id
    JOIN product p ON co.product_id = p.id
    WHERE co.business_id=%s
      AND co.order_status=%s;
    """
    cursor.execute(query, (business_id,"pending"))
    return f"""{cursor.fetchall()}"""


get_supplier_id_by_name.__doc__ = f"""
    Returns supplier id
    Args:
        business_id (int): ID of the business
        name(str): Name of the supplier
        
    Returns:
        the supplier id, returns -1 if not found
    """

add_supply_order.__doc__ = f"""
    Add an order to supply_order
    The value of `item_name`, `item_brand`, `supplier_name` class parameters must be formatted in the following way:
        {params_format()}

    Args:
        item_name(str) : Name of the item
        item_brand(str) : brand of the item
        business_id(str) : id of the business
        supplier_name(str) : Name of the Supplier
        quantity(int) : Quantity of items to be supplied
        supplier_id(int) : ID of the supplier, use only if you have the ID

    """

get_unfulfilled_supplier_order.__doc__ = f"""
    Returns unfulfilled supplier orders
    
    Args:
    business_id[str] : ID of the business

    
    Returns:
        Unfulfilled supplier Orders
    """

get_unfulfilled_customer_orders.__doc__ = f"""
    Returns unfulfilled customer orders
    
    Args:
    business_id[str] : ID of the business

    Returns:
        Unfulfilled Customer Orders
    """
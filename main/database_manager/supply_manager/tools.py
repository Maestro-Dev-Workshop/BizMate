import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','..')))
from database_manager.tools import *

def add_supplier(business_name:str,
                name:str,
                contact_det: str, 
                product_ids: list[str],
                cost_prices: list[str],
                available:list[str]) -> dict:
    """
    Add supplier details to the database, along with their products

    Args:
        name(str): Name of the supplier
        contact_det(str): the contact details of the supplier
        product_ids(str): a list containing id of the products the supplier supplies
        cost_prices: a list containing the cost price of the products
        available: a list containing whether a product is available

    Returns:
        a dictionary which states whether an operation was successfull of not
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    supplier_cols = "(business_id, name, contact_details)"
    supp_fmt = "%s, %s, %s"
    inv_cols = "(product_id,supplier_id,cost_price,available)"
    inv_fmt = "%s, %s, %s, %s"
    message = {}
    supplier_vals = (business_id,name, contact_det)
    message[f"supplier:{name}"] = insert("supplier", supplier_cols, supplier_vals, supp_fmt)
    cursor.execute("""SELECT id from supplier WHERE business_id=%s AND contact_details=%s""",(business_id,contact_det))
    supplier_id = cursor.fetchone()[0]
    for ind, product in enumerate(product_ids):
        inv_vals = (product, supplier_id, cost_prices[ind], available[ind])
        message[f"product_id {product} from supplier {name}"] = insert("supplier_inventory",inv_cols,inv_vals,inv_fmt)
    return message

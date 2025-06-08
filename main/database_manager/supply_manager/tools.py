import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.tools import *

def add_supplier(business_name:str,
                name:str,
                contact_det: str, 
                product_names: list[str],
                product_brands: list[list[str]],
                cost_prices: list[str],
                available:list[str]) -> dict:
    """
    Add supplier details to the database, along with their products

    Args:
        name(str): Name of the supplier
        contact_det(str): the contact details of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands(str): a list of list containing brands of the products the supplier supplies
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
    product_ids = get_product_id(product_names,product_brands)
    for ind, product in enumerate(product_ids):
        inv_vals = (product, supplier_id, cost_prices[ind], available[ind])
        message[f"product_id {product} from supplier {name}"] = insert("supplier_inventory",inv_cols,inv_vals,inv_fmt)
    return message

def get_product_id(
        business_name : str,
        product_name : list[str],
        product_brand : list[list[str]]
):
    business_id = get_single_value("business", "business_name", business_name, "id")
    product_ids = []
    for ind,name in enumerate(product_name):
        for brand in product_brand[ind]:
            query = """SELECT id FROM product WHERE business_id=%s AND item_name= %s AND brand = %s"""
            cursor.execute(query, (business_id,name, brand))
            val = cursor.fetchone()
            product_ids.append(val[0])
    return product_ids

def get_no_suppliers() -> str:
    """Returns Products with no Suppliers"""
    cursor.execute("""SELECT p.id, p.item_name, p.brand
        FROM product p
        LEFT JOIN supplier_inventory si ON p.id = si.product_id
        WHERE si.supplier_id IS NULL;""")
    return f"""{cursor.fetchall()}"""
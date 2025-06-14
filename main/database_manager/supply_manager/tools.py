import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.tools import *

def add_supplier(business_name:str,
                name:str,
                contact_det: str, 
                ) -> dict:
    f"""
    Add supplier details to the database

    Args:
        business_name (str): name of the business
        name(str): Name of the supplier
        contact_det(str): the contact details of the supplier

    business_name and name value must be formatted in the following way:
     {params_format()}
    Returns:
        a dictionary which states whether an operation was successful of not
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    supplier_cols = "(business_id, name, contact_details)"
    supp_fmt = "%s, %s, %s"
    message = {}
    supplier_vals = (business_id,name, contact_det)
    supplier_id = get_supplier_id_by_mail(business_id,contact_det)
    if (supplier_id == -1):
        message[f"supplier:{name}"] = insert("supplier", supplier_cols, supplier_vals, supp_fmt)
    else:
        message[f"supplier:{name}"] = "Supplier already exists"
    return message

def get_supplier_id_by_mail(business_name:int,
                name: str) -> int:
    f"""
    Returns supplier id

    Args:
        business_name (str): name of the business
        name(str): Name of the supplier
    
    business_name and name value must be formatted in the following way:
     {params_format()}
        
    Returns:
        the supplier id, returns -1 if not found
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    cursor.execute("""SELECT id from supplier WHERE business_id=%s AND contact_details=%s""",(business_id,name))
    supplier_id = cursor.fetchall()
    cursor.reset()
    if len(supplier_id) > 1:
        return -1
    elif len(supplier_id) == 1:
        return supplier_id[0][0]
    else:
        return -1

def get_supplier_inv_id(supplier_id : int,
                        product_id : int) -> int:

    cursor.execute("""SELECT * from supplier_inventory WHERE supplier_id=%s AND product_id=%s""",(supplier_id,product_id))
    try:
        found = len(cursor.fetchone())
        cursor.reset()
        return 1
    except TypeError:
        0
    """
    Returns inventory id of  the suppliers
    """

def get_product_id(
        business_id:int,
        product:str,
        brand:str) -> int:
    f"""Gets the id for a product
    Args:
        business_id(str): Business id
        product(str): name of the product
        brand(str) : brand of the product

    product and brand value must be formatted in the following way:
     {params_format()}
    
    Returns:
        id of the product, -1 if not found
    """
    query = """SELECT id FROM product WHERE business_id=%s AND item_name= %s AND brand =%s"""
    cursor.execute(query, (business_id,product, brand))
    try:
        product_id = cursor.fetchone()[0]
        cursor.reset()
        return product_id
    except Exception as e:
        return -1

def add_to_supplier_inv(
                business_name:str,
                contact_detail:str,
                product_names: list[str],
                product_brands: list[list[str]],
                cost_prices: list[list[int]],
                available:list[list[bool]]) -> dict:
    f"""
    Add supplier details to the database

    Args:
        business_name(str): Name of the business
        contact_detail(str): the contact_detail of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
        cost_prices(list[list(str)]): a list of list containing cost prices of items by brands of the products
        available(list[list[bool]]): a list of list containing a product by brand is availability

    The values of business_name, product_names, product_brands must be formatted in the following way:
    {params_format()}
    Returns:
        a dictionary which states whether an operation was successful of not
    """
    inv_cols = "(product_id,supplier_id,cost_price,available)"
    inv_fmt = "%s, %s, %s, %s"
    message = {}
    business_id = get_single_value("business", "business_name", business_name, "id")
    supplier_id = get_supplier_id_by_mail(business_name,contact_detail)
    for ind, product in enumerate(product_names):
        for j,brand in enumerate(product_brands[ind]):
            product_id = get_product_id(business_id,product,brand)
            if product_id == -1:
                message[f"product_id {product} from supplier_id {supplier_id}"] = f"{product}({brand}) not existing on inventory"
            
            elif get_supplier_inv_id(supplier_id,product_id):
                message[f"product_id {product} from supplier_id {supplier_id}"] = f"{product}({brand}) already exist"
            else:
                inv_vals = (product_id, supplier_id, cost_prices[ind][j], available[ind][j])
                message[f"product_id {product} from supplier_id {supplier_id}"] = insert("supplier_inventory",inv_cols,inv_vals,inv_fmt)
    return message

def add_supplier_and_suppier_inv(
        business_name:str,
        supplier_name:str,
        contact_det:str,
        product_names: list[str],
        product_brands: list[list[str]],
        cost_prices: list[list[int]],
        available:list[list[bool]]) -> dict:
    f"""
    Adds to both supplier and supplier inventory

    Args:
        business_name(str): Name of the business
        supplier_name(str): Name of the supplier
        contact_det(str): the contact details of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
        cost_prices(list[list(str)]): a list of list containing cost prices of items by brands of the products
        available(list[list[bool]]): a list of list containing a product by brand is availability
    
    The values of business_name, supplier_name, product_names, product_brands must be formatted in the following way:
    {params_format}
    Returns:
        a dictionary which states whether an operation was successful of not
    """
    message = add_supplier(business_name,supplier_name,contact_det) | add_to_supplier_inv(business_name,contact_det,product_names,product_brands,cost_prices,available)
    return message

def get_no_suppliers() -> str:
    """Returns Products with no Suppliers"""
    cursor.execute("""SELECT p.id, p.item_name, p.brand
        FROM product p
        LEFT JOIN supplier_inventory si ON p.id = si.product_id
        WHERE si.supplier_id IS NULL;""")
    return f"""{cursor.fetchall()}"""

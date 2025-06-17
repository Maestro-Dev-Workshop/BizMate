import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.tools import *

def add_supplier(business_name:str,
                name:str,
                contact_det: str, 
                ) -> dict:
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

def get_supplier_id_by_mail(business_name:str,
                name: str) -> int:
    business_id = get_single_value("business", "business_name", business_name, "id")
    cursor.execute("""SELECT id FROM supplier WHERE business_id=%s AND contact_details=%s""",(business_id,name))
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
    message = add_supplier(business_name,supplier_name,contact_det) | add_to_supplier_inv(business_name,contact_det,product_names,product_brands,cost_prices,available)
    return message

def get_no_suppliers() -> str:
    """Returns Products with no Suppliers"""
    cursor.execute("""SELECT p.id, p.item_name, p.brand
        FROM product p
        LEFT JOIN supplier_inventory si ON p.id = si.product_id
        WHERE si.supplier_id IS NULL;""")
    return f"""{cursor.fetchall()}"""

def delete_supplier_inv(
                business_name:str,
                contact_detail:str,
                product_names: list[str],
                product_brands: list[list[str]],
                ) -> dict:
    message = {}
    business_id = get_single_value("business", "business_name", business_name, "id")
    supplier_id = get_supplier_id_by_mail(business_name,contact_detail)
    for ind, product in enumerate(product_names):
        for j,brand in enumerate(product_brands[ind]):
            product_id = get_product_id(business_id,product,brand)
            if product_id == -1:
                message[f"product_id {product_id} from supplier_id {supplier_id}"] = f"{product}({brand}) not existing on inventory"
            else:
                message[f"product_id {product_id} from supplier_id {supplier_id}"] = delete_row("supplier_inventory",["product_id","supplier_id"],[product_id,supplier_id])
    return message

def delete_supplier(business_name:str,
                name:str,
                contact_det: str, 
                ) -> dict:
    business_id = get_single_value("business", "business_name", business_name, "id")
    message = {}
    supplier_id = get_supplier_id_by_mail(business_name,contact_det)
    if (supplier_id == -1):
        message[f"supplier:{name}"] = "Supplier doesn't exist"
    else:
        message[f"supplier:{name}"] = delete_row("supplier",["business_id","id"],[business_id,supplier_id])
    return message

def delete_supplier_and_supplier_inv(
        business_name:str,
        supplier_name:str,
        contact_det:str,
        product_names: list[str],
        product_brands: list[list[str]]) -> dict:
    message = delete_supplier_inv(business_name,contact_det,product_names,product_brands)
    message = message | delete_supplier(business_name,supplier_name,contact_det)
    return message

def view_suppliers(business_name : str):
    """
    Retrieves all suppliers with their associated business names and contact details.

    Returns:
        list of dict: Each dict contains supplier info (name, contact, business name).
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    query = """
    SELECT s.id AS supplier_id,
           s.name AS supplier_name,
           s.contact_details AS supplier_contact
    FROM supplier s
    JOIN business b ON b.id = %s
    """
    try:
        cursor.execute(query, (business_id,))
        results = cursor.fetchall()
        return f"""{results}"""
    except Exception as e:
        return f"Error fetching suppliers: {e}"

def view_supplier_inventory(business_name :str):
    """
    Retrieves supplier inventory including product and supplier information.

    Returns:
        list of dict: Each dict contains product name, brand, supplier name, cost price, and availability.
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    query = """
    SELECT 
        s.name AS supplier_name,
        si.product_id,
        p.item_name,
        p.brand,
        si.cost_price,
        si.available
    FROM supplier_inventory si
    JOIN product p ON si.product_id = p.id
    JOIN supplier s ON si.supplier_id = s.id
    WHERE s.business_id = %s
    """
    try:
        cursor.execute(query,(business_id,))
        results = cursor.fetchall()
        return f"""{results}"""
    except Exception as e:
        return f"Error fetching supplier inventory: {e}"

def get_single_supplier_inventory(business_name :str, contact_detail: str):
    """
    Retrieves supplier inventory including product and supplier information.

    Returns:
        list of dict: Each dict contains product name, brand, supplier name, cost price, and availability.
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    supplier_id = get_supplier_id_by_mail(business_name,contact_detail)
    query = """
    SELECT 
        s.name AS supplier_name,
        s.contact_details,
        si.product_id,
        p.item_name,
        p.brand,
        si.cost_price,
        si.available
    FROM supplier_inventory si
    JOIN product p ON si.product_id = p.id
    JOIN supplier s ON s.id = si.supplier_id
    WHERE s.business_id = %s AND s.id=%s
    """
    try:
        cursor.execute(query,(business_id,supplier_id))
        results = cursor.fetchall()
        return f"""{results}"""
    except Exception as e:
        return f"Error fetching supplier inventory: {e}"

#Docstrings
add_supplier.__doc__ = f"""
    Add supplier details to the database

    The value of `business_name` and `name` must be formatted in the following way:
        {params_format()}
    Args:
        business_name (str): name of the business
        name(str): Name of the supplier
        contact_det(str): the contact details of the supplier

    Returns:
        a dictionary which states whether an operation was successful of not
    """

get_supplier_id_by_mail.__doc__ = f"""
    The value of `business_name` and `name` value must be formatted in the following way:
        {params_format()}

    Returns supplier id

    Args:
        business_name (str): name of the business
        name(str): Name of the supplier


    Returns:
        the supplier id, returns -1 if not found
    """

get_supplier_inv_id.__doc__ = """
    Returns inventory id of the suppliers
    """

get_product_id.__doc__ = f"""Gets the id for a product
    The values of `product` and `brand` must be formatted in the following way:
        {params_format()}
    Args:
        business_id(str): Business id
        product(str): name of the product
        brand(str) : brand of the product

    Returns:
        id of the product, -1 if not found
    """

add_to_supplier_inv.__doc__ = f"""
    Add inventory of supplier to the database

    The values of `business_name`, `product_names`, `product_brands` must be formatted in the following way:
        {params_format()}
    Args:
        business_name(str): Name of the business
        contact_detail(str): the contact_detail of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
    Returns:
        a dictionary which states whether an operation was successful of not
    """

add_supplier_and_suppier_inv.__doc__ = f"""
    Adds to both supplier and supplier inventory
    The values of `business_name`, `supplier_name`, `product_names`, `product_brands` must be formatted in the following way:
        {params_format}
    Args:
        business_name(str): Name of the business
        supplier_name(str): Name of the supplier
        contact_det(str): the contact details of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
        cost_prices(list[list(str)]): a list of list containing cost prices of items by brands of the products
        available(list[list[bool]]): a list of list containing a product by brand is availability

    Returns:
        a dictionary which states whether an operation was successful of not
    """

delete_supplier.__doc__ = f"""
    Deletes supplier details from the database

    The value of `business_name` and `name` must be formatted in the following way:
        {params_format()}
    Args:
        business_name (str): name of the business
        name(str): Name of the supplier
        contact_det(str): the contact details of the supplier

    Returns:
        a dictionary which states whether an operation was successful of not
    """

delete_supplier_inv.__doc__ = f"""

    Deletes an inventory from the supplier to the database

    The values of `business_name`, `product_names`, `product_brands` must be formatted in the following way:
        {params_format()}
    Args:
        business_name(str): Name of the business
        contact_detail(str): the contact_detail of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
    Returns:
        a dictionary which states whether an operation was successful of not
    """

delete_supplier_and_supplier_inv.__doc__ = f"""
    Deletes from both supplier and supplier inventory
    The values of `business_name`, `supplier_name`, `product_names`, `product_brands` must be formatted in the following way:
        {params_format}
    Args:
        business_name(str): Name of the business
        supplier_name(str): Name of the supplier
        contact_det(str): the contact details of the supplier
        product_names(str): a list containing names of the products the supplier supplies
        product_brands (list[list[str]]): a list of list containing brands of the products the supplier supplies
    Returns:
        a dictionary which states whether an operation was successful of not
    """

view_suppliers.__doc__ = f"""
Returns the Supplier details a business has

The value of `business_name` parameter must be formatted in the following way:

Args:
    business_name : The name of the business to filter result

Returns:
    (supplier_id, supplier_name, supplier_contact)
"""

view_supplier_inventory.__doc__ =  f"""
Returns all the Supplier details and the product they supply for a business

The value of `business_name` parameter must be formatted in the following way:

Args:
    business_name : The name of the business to filter result

Returns:
    (supplier_name, product_id, item_name, brand, cost_price, availability)
"""

get_single_supplier_inventory.__doc__ = f"""

Returns a specific supplier detail and the product they supply for a business

The value of `business_name` parameter must be formatted in the following way:

Args:
    business_name : The name of the business to filter result


Returns:
    (supplier_name, supplier_contact_details,product_id, item_name, brand, cost_price, availability)"""


print(delete_supplier_inv("numina_analytics","tech@technovasupplies.com",["wireless_mouse"],[["TechGear"]]))
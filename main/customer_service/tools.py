import sys
import os
import datetime
from collections.abc import Iterable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_manager.tools import *


def get_business_info(
        business_id: str
):
    """
    Get some basic information about the business.
    
    Args:
        business_id (str): the id of the business to search for (in string format).
    Returns:
        A dictionary containing information about the business, including business_name, brief_description, date_joined, contact_details, and physical_address.
    """

    cols = ["business_name", "brief_description", "date_joined", "contact_details", "physical_address"]
    result = get_rows_with_exact_column_values(
        "business", 
        ["id"], 
        [business_id], 
        cols)[0]
    
    if isinstance(result, str):
        return result
    else:
        return {cols[i]: result[i] for i in range(len(cols))}


def get_products_info(
        business_id: str
):
    """
    Get the details of all the products a business offers.
    
    Args:
        business_id (str): the id of the business to search for (in string format).
    Returns:
        A list of dictionaries, each representing a product, with keys: item_name, category, brand, quantity_in_stock, selling_price, and minimum_selling_price.
    """

    cols = ["item_name", "category", "brand", "quantity_in_stock", "selling_price", "minimum_selling_price"]
    result = get_rows_with_exact_column_values(
        "product", 
        ["business_id"], 
        [business_id], 
        cols)
    # print(result)
    
    if isinstance(result, str):
        return result
    else:
        products = []
        for prod in result:
            products.append({cols[i]: prod[i] for i in range(len(cols))})
        return products


def get_specific_product_info(
        business_id: str,
        product_id: str | None = None,
        product_name: str | None = None,
):
    """
    Get details of a specific product by searching, either by the product's id, or the name provided.

    Args:
        business_id (str): the id of the business to search for (in string format).
        (optional) product_id (str): the id of the product to search for.
        (optional) product_name (str): the name of the product.
        Note: Either the product_id or product_name must be provided, both cannot be empty.
    Returns:
        A list of dictionaries, each representing a product with matching name/id, with keys: item_name, category, brand, quantity_in_stock, selling_price, and minimum_selling_price.
    """

    cols = ["item_name", "category", "brand", "quantity_in_stock", "selling_price", "minimum_selling_price"]

    if product_id:
        result = get_rows_with_exact_column_values(
        "product", 
        ["business_id", "id"], 
        [business_id, product_id], 
        cols)

    elif product_name:
        pre_result = get_rows_with_matching_column_values(
        "product", 
        ["item_name"], 
        [product_name], 
        ["business_id"] + cols)

        result = []
        if isinstance(pre_result, str):
            result = pre_result
        else:
            for prod in pre_result:
                if str(prod[0]) == business_id:
                    result.append(prod[1:])

    else:
        return "Error: Neither product_id nor product_name was provided"
    
    if isinstance(result, str):
        return result
    else:
        products = []
        for prod in result:
            products.append({cols[i]: prod[i] for i in range(len(cols))})
        return products


def get_customer_details():
    """Get details of a customer"""
    pass

def upload_customer_details(
        business_id: str
):
    """Upload details of a customer to the database"""
    pass

def get_customer_visits(
        business_id: str
):
    """Gets information of a customer's visits up to a certain timestamp"""
    pass

def get_all_customer_visits(
        business_id: str
):
    """Gets records of all the customer's visits"""
    pass

def log_customer_visit(
        business_id: str
):
    """Upload details of a customer's visit, including datetime of visit, summary of queries made, and number of order(s) made (if any)"""
    pass

def get_customer_orders(
        business_id: str
):
    """Get the records of a customer's orders, up to a certain timestamp"""
    pass

def get_all_customer_orders(
        business_id: str
):
    """Get all records of a customer's orders"""
    pass

def upload_customer_order(
        business_id: str
):
    """Upload details of a customer's order to the database"""
    pass

# print(get_business_info("1"))
# print(get_products_info("1"))
# print(get_specific_product_info("1", product_name="Toothbrush"))
# print(get_specific_product_info("1", product_id="3"))
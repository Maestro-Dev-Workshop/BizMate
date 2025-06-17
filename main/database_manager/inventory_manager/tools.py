import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.tools import *
import datetime

def add_item(
        business_name:str,
        item_names:list[str],
        categories: list[str],
        brands:list[list[str]],
        min_thresholds:list[list[str]],
        quantities: list[list[int]],
        sps: list[list[float]],
        min_selling_prices: list[list[float]],
        expiry_dates: list[list[str]],
        metadata : list[list[str]]
) -> dict:
    business_id = get_single_value("business", "business_name", business_name, "id")
    expiry_dates = [[datetime.datetime.strptime(exp, "%Y-%m-%d").date() for exp in sublist] for sublist in expiry_dates]
    cols = (brands, quantities, min_thresholds, sps, min_selling_prices, expiry_dates, metadata)
    columns = "(business_id, item_name, category, brand, quantity_in_stock, minimum_threshold, selling_price, minimum_selling_price, expiry_date, metadata, active)"
    fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    message = {}
    for ind in range(len(item_names)):
        for sub_ind in range(len(brands[ind])):
            row = [business_id, item_names[ind], categories[ind]] + [col[ind][sub_ind] for col in cols] + [1]
            message[f"{item_names[ind]}, brand: {brands[ind][sub_ind]}"] = insert("product", columns, row, fmt)
    return message


def get_expired_goods(business_name: str):
    business_id = get_single_value("business", "business_name", business_name, "id")
    query = "SELECT * FROM product WHERE expiry_date < CURDATE() AND business_id= %s AND active=1"
    cursor.execute(query,(business_id,))
    return f"Expired Goods : {cursor.fetchall()}"

def get_minimum_threshold(business_name: str):
    """Returns Items below minimum threshold"""
    business_id = get_single_value("business", "business_name", business_name, "id")
    query = "SELECT * FROM product WHERE quantity_in_stock <= minimum_threshold AND business_id= %s AND active=1"
    cursor.execute(query, (business_id,))
    return f"Items below minimum threshold: {cursor.fetchall()}"

def view_items(business_name: str):
    business_id = get_single_value("business", "business_name", business_name, "id")
    query = "SELECT * FROM product WHERE business_id= %s AND active=1"
    cursor.execute(query, (business_id,))
    return f"Items are: {cursor.fetchall()}"

view_items.__doc__ = f"""
Returns all the item for a business
The value of `business_name` parameter must be formatted in the following way:
{params_format()}
Args:
    business_name(str) : Name of the business

Returns:
    the items available

"""

get_expired_goods.__doc__ = f"""Returns Expired Goods
business_name must be formatted as {params_format}

business_name (str) : Name of the business

"""

get_minimum_threshold.__doc__ = f"""Returns Items below minimum threshold
business_name must be formatted as {params_format}

business_name (str) : Name of the business

"""


add_item.__doc__ = f"""
    Adds products to the products table

    The values of `business_name`, `item_names`, `categories` and `brands` must be formatted in the following way:
        {params_format()}

    Args:
    business_name(str): name of the business that owns such item
    item_names(list[str]): list of items to add to the table
    categories(list[str]): contains the categories of each item
    brands(list[list[str]]): list of lists, in which for each list contains the available brand for an item
    min_thresholds(list[list[str]]): list of lists, in which for each list contains the minimum threshold for an item
    quantities(list[list[int]]): list of lists, in which for each list contains the quantity available for an item
    selling_price(list[list[float]]) : list of lists, in which for each list contains the price available for an item
    min_selling_price(list[list[float]]) : list of lists, in which for each list contains the percentage of negotiation available for an item
    expiry_date(list[list[str]]) : list of lists, in which for each list contains the expiry date for an item
    metadata(list[list[str]]) : list of lists, in which for each list contains other information about an item.

    Returns
    A dict containing whether an item with a specific brand was added to the database
    
    """

get_expired_goods.__doc__ = f"""
Get Expired Goods for a business

The values of `business_name` must be formatted in the following way:
        {params_format()}

Args:
    business_name(str): name of the business that owns such item

Returns
    A list of expired goods
"""


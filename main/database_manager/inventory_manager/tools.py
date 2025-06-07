import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','..')))
from database_manager.tools import *
import datetime

def add_item(
        business_name:str,
        item_names:list[str],
        categories: list[str],
        brands:list[list[str]],
        quantities: list[list[int]],
        sps: list[list[float]],
        negotiate_percents: list[list[float]],
        expiry_dates: list[list[str]],
        metadata : list[list[str]]
) -> dict:
    """
    Adds products to the products table

    Args:
    business_name(str): name of the business that owns such item
    item_names(list[str]): list of items to add to the table
    categories(list[str]) : contains the category for each item
    brand(list[list[str]]): list of lists, in which for each list contains the available brand for an item
    quantities(list[list[int]]): list of lists, in which for each list contains the quantity available for an item
    selling_price(list[list[float]]) : list of lists, in which for each list contains the price available for an item
    negotiate_percent(list[list[float]]) : list of lists, in which for each list contains the percentage of negotiation available for an item
    expiry_date(list[list[str]]) : list of lists, in which for each list contains the expiry date for an item
    metadata(list[list[str]]) : list of lists, in which for each list contains other information about an item.

    Returns
    A dict containing whether an item with a specific brand was added to the database
    
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    cols = (brands, quantities, sps, negotiate_percents, expiry_dates, metadata)
    expiry_dates = [[datetime.datetime.strptime(exp, "%Y-%m-%d").date() for exp in sublist] for sublist in expiry_dates]
    columns = "(business_id, item_name, category, brand, quantity_in_stock, selling_price, negotiate_percent, expiry_date, metadata)"
    fmt = fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s"
    message = {}
    for ind in range(len(item_names)):
        for sub_ind in range(len(brands[ind])):
            row = [business_id, item_names[ind], categories[ind]] + [col[ind][sub_ind] for col in cols]
            message[f"{item_names[ind]}, brand: {brands[ind][sub_ind]}"] = insert("product", columns, row, fmt)
    return message

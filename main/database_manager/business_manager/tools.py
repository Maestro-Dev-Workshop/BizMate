import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from database_manager.db_utils import db, cursor
from database_manager.tools import *
import datetime

def add_product(
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
    manufacturer(list[list[str]]): list of lists, in which for each list contains the available manufacturer for an item
    quantities(list[list[int]]): list of lists, in which for each list contains the quantity available for an item 
    selling_price(list[list[float]]) : list of lists, in which for each list contains the price available for an item 
    negotiate_percent(list[list[float]]) : list of lists, in which for each list contains the percentage of negotiation available for an item 
    expiry_date(list[list[str]]) : list of lists, in which for each list contains the expiry date for an item 
    metadata(list[list[str]]) : list of lists, in which for each list contains other information about an item.

    Returns
    A dict containing whether an item with a specific manufacturer was added to the database
    
    """
    business_id = get_single_value("business", "business_name", business_name, "id")
    cols = (brands, quantities, sps, negotiate_percents, expiry_dates, metadata)
    expiry_dates = [[datetime.datetime.strptime(exp, "%Y-%m-%d").date() for exp in sublist] for sublist in expiry_dates]
    columns = "(business_id, item_name, category, manufacturer, quantity_in_stock, selling_price, negotiate_percent, expiry_date, metadata)"
    fmt = fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s"
    message = {}
    for ind in range(len(item_names)):
        for sub_ind in range(len(brands[ind])):
            row = [business_id, item_names[ind], categories[ind]] + [col[ind][sub_ind] for col in cols]
            message[f"{item_names[ind]}, Manufacturer: {brands[ind][sub_ind]}"] = insert("product", columns, row, fmt)
    return message


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


def delete_business(business_name : str) ->str:
    """Updates active column to false
    
    Args:
        business_name(str): Name of the business
    
    Returns
        whether the update operation was successful or not
    """
    return update_table("business",["business_name"],[business_name],["active"],[False])

def verify_business(business_name: str) -> str:
    """Verifies if the business exist then it returns the id
    
    Args:
        business_name(str): name of the business
    
    Returns:
        the id of the business if it exists
    """
    id = get_single_value("business", "business_name", business_name, "id"),
    active = get_single_value("business", "business_name", business_name, "active")
    if isinstance(active,int):
        return id if active else "Does not Exist"
    else:
        return "Does Not Exist"



# print(
#     add_product(
#         "GS",
#         item_names=["Cement", "Vegetable Oil"],
#         brands=[["Dangote", "Lafarge"],["King", "Mamador"]],
#         quantities=[[200,20],[10,5]],
#         sps=[[11000,14000],[4000,2000]],
#         negotiate_percents=[[0,0],[3,2]],
#         expiry_dates=[["2030-03-04","2036-04-05"],["2026-03-30","2025-02-20"]],
#         metadata=[["10kg","In half bags"], ["20kg","2kg"]]
#     )
# )

# print(add_supplier(
#         "GS",
#         name="SG",
#         contact_det="0402345453",
#         product_ids=["1","2","3","4"],
#         cost_prices=[10000,5000,2300,1000],
#         available=[True,False,False,True]
#     )
# )

# print(verify_business("GS"))
# print(verify_business("rveim"))
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


def get_customer_details(
        username: str
):
    """
    Get details of a customer.

    Args:
        username (str): the telegram username of the customer.
    Returns:
        A dictionary containing details of the customer, with keys: id, username, name, age, gender, contact_details.
    """

    cols = ["id","username", "name", "age", "gender", "contact_details"]
    result = get_rows_with_exact_column_values(
        "customer", 
        ["username"], 
        [username], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        return {cols[i]: result[0][i] for i in range(len(cols))}


def upload_customer_details(
        username: str,
        name: str,
        age: int,
        gender: str,
        contact_details,
):
    """
    Uploads details of a customer to the database

    Args:
        username (str): the telegram username of the customer.
        name (str): the first and last name of the customer.
        age (int): the age of the customer.
        gender (str): the gender of the customer (as M for male or F for female).
        contact_details (str): the phone number or other contact detail of the customer.
    Return:
        A response notifying whether or not record upload was successful
    """
    tbl_name = "customer"
    cols = ["username", "name", "age", "gender", "contact_details"]
    values = (username, name, age, gender, contact_details)
    values_fmt = "%s, %s, %s, %s, %s"
    result = insert(tbl_name, cols, values, values_fmt)
    return result


def get_customer_visits(
        business_id: str,
        customer_id: str,
        start_date: str,
):
    """
    Gets information of a customer's visits up to a certain timestamp
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        start_date (str): the date to filter from, in the format YYYY-mm-dd.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: date_of_visit, summary, and orders_made.
    """

    cols = ["date_of_visit", "summary", "orders_made"]
    query = f"SELECT {', '.join(cols)} FROM visit WHERE business_id = %s AND customer_id = %s AND date_of_visit >= %s"
    try:
        cursor.execute(query, (business_id, customer_id, start_date))
        result = cursor.fetchall()
        visits = []
        for visit in result:
            visits.append({cols[i]: visit[i] for i in range(len(cols))})
        return visits
    except Exception as e:
        return f"Error: {e}"


def get_all_customer_visits(
        business_id: str,
        customer_id: str
):
    """
    Gets records of all the customer's visits
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: date_of_visit, summary, and orders_made.
    """

    cols = ["date_of_visit", "summary", "orders_made"]
    result = get_rows_with_exact_column_values(
        "visit", 
        ["business_id", "customer_id"], 
        [business_id, customer_id], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        visits = []
        for visit in result:
            visits.append({cols[i]: visit[i] for i in range(len(cols))})
        return visits


def log_customer_visit(
        business_id: str,
        customer_id: str,
        summary: str,
        orders_made: int,
):
    """
    Upload details of a customer's visit, including datetime of visit, summary of queries made, and number of order(s) made (if any)

    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        summary (str): a condensed summary of the queries made by the user during the session.
        orders_made (int): the number of orders made by the user during the session.
    Returns:
        A response notifying whether or not record upload was successful.
    """

    tbl_name = "visit"
    cols = ["customer_id", "business_id", "date_of_visit", "visit_summary", "orders_made"]
    time_of_visit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = (customer_id, business_id, time_of_visit, summary, orders_made)
    values_fmt = "%s, %s, %s, %s, %s"
    result = insert(tbl_name, cols, values, values_fmt)
    return result


def get_customer_orders(
        business_id: str,
        customer_id: str,
        start_date: str
):
    """
    Get the records of a customer's orders, up to a certain timestamp
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        start_date (str): the date to filter from, in the format YYYY-mm-dd.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: product_id, quantity_ordered, discount_factor, and date_ordered.
    """

    cols = ["product_id", "quantity_ordered", "discount_factor", "date_ordered"]
    query = f"SELECT {', '.join(cols)} FROM customer_order WHERE business_id = %s AND customer_id = %s AND date_ordered >= %s"
    try:
        cursor.execute(query, (business_id, customer_id, start_date))
        result = cursor.fetchall()
        orders = []
        for order in result:
            orders.append({cols[i]: order[i] for i in range(len(cols))})
        return orders
    except Exception as e:
        return f"Error: {e}"


def get_all_customer_orders(
        business_id: str,
        customer_id: str
):
    """
    Get all records of a customer's orders
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
    Returns:
        A list of dictionaries, each representing a customer's order, with keys: product_id, quantity_ordered, discount_factor, and date_ordered.
    """

    cols = ["product_id", "quantity_ordered", "discount_factor", "date_ordered"]
    result = get_rows_with_exact_column_values(
        "customer_order", 
        ["business_id", "customer_id"], 
        [business_id, customer_id], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        orders = []
        for order in result:
            orders.append({cols[i]: order[i] for i in range(len(cols))})
        return orders


def upload_customer_order(
        business_id: str,
        customer_id: str,
        product_id: str,
        quantity_ordered: int,
        discount_factor: float
):
    """
    Upload details of a customer's order to the database
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        product_id (str): the id of the product being ordered.
        quantity_ordered (int): the amout of the product to order.
        discount_factor (float): the percentage of discount being applied to the order (ranging from 0.0 as no discount to 1.0 as 100% discount).
    Returns:
        A response notifying whether or not record upload was successful.
    """

    tbl_name = "visit"
    cols = ["customer_id", "business_id", "product_id", "quantity_ordered", "discount_factor", "date_ordered"]
    time_of_order = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = (customer_id, business_id, product_id, quantity_ordered, discount_factor, time_of_order)
    values_fmt = "%s, %s, %s, %s, %s, %s"
    result = insert(tbl_name, cols, values, values_fmt)


# print(get_business_info("1"))
# print(get_products_info("1"))
# print(get_specific_product_info("1", product_name="Toothbrush"))
# print(get_specific_product_info("1", product_id="3"))
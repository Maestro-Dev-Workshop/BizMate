import sys
import os
from google.adk.tools import ToolContext
from main.utils.db_utils import (cursor,get_rows_with_matching_column_values,
                                get_rows_with_exact_column_values, insert,list_tables,describe_table,
                                execute_query,get_single_value,params_format)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime


def get_business_info(
        business_id: str
):
    """
    Specialized Customer Service Agent Tool.
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
        cols)
    
    if isinstance(result, str):
        return result
    else:
        return {cols[i]: result[0][i] for i in range(len(cols))}


def get_products_info(
        business_id: str
):
    """
    Specialized Customer Service Agent Tool.
    Get the details of all the products a business offers.
    
    Args:
        business_id (str): the id of the business to search for (in string format).
    Returns:
        A list of dictionaries, each representing a product, with keys: id, item_name, category, brand, quantity_in_stock, selling_price, and minimum_selling_price.
    """

    cols = ["id", "item_name", "category", "brand", "quantity_in_stock", "selling_price", "minimum_selling_price"]
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
        product_id: str,
        product_name: str,
):

    cols = ["id", "item_name", "category", "brand", "quantity_in_stock", "selling_price", "minimum_selling_price"]

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
        id: str
):
    """
    Specialized Customer Service Agent Tool.
    Get details of a customer.

    Args:
        username (str): the telegram username of the customer.
    Returns:
        A dictionary containing details of the customer, with keys: id, username, name, age, gender, contact_details.
    """

    cols = ["id","username", "name", "age", "gender", "contact_details"]
    result = get_rows_with_exact_column_values(
        "customer", 
        ["id"], 
        [id], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        if result:
            return {cols[i]: result[0][i] for i in range(len(cols))}
        else:
            return "Customer record not found"


def upload_customer_details(
        id : str,
        business_id: str,
        username: str,
        name: str,
        age: int,
        gender: str,
        contact_details: str,
        tool_context: ToolContext
):
    tbl_name = "customer"
    chat_id = tool_context.state.get("chat_id", None)
    cols = ["id","username", "name", "age", "gender", "contact_details"]
    cols = f"({', '.join(cols)})"
    values = (id,username, name, age, gender, contact_details)
    values_fmt = "%s, %s, %s, %s, %s, %s, %s"
    result = insert(tbl_name, cols, values, values_fmt)

    cols = ["customer_id", "chat_id", "business_id"]
    cols = f"({', '.join(cols)})"
    values = (id, chat_id, business_id)
    values_fmt = "%s, %s, %s"
    insert("chat", cols, values, values_fmt)
    return result


def get_customer_visits(
        business_id: str,
        customer_id: str,
        start_date: str,
):
    """
    Specialized Customer Service Agent Tool.
    Gets information of a customer's visits up to a certain timestamp
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        start_date (str): the date to filter from, in the format YYYY-mm-dd.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: date_of_visit, visit_summary, and orders_made.
    """

    cols = ["date_of_visit", "visit_summary", "orders_made"]
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
    Specialized Customer Service Agent Tool.
    Gets records of all the customer's visits
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: date_of_visit, visit_summary, and orders_made.
    """

    cols = ["date_of_visit", "visit_summary", "orders_made"]
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
    Specialized Customer Service Agent Tool.
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
    cols = f"({', '.join(cols)})"
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
    Specialized Customer Service Agent Tool.
    Get the records of a customer's orders, up to a certain timestamp
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        start_date (str): the date to filter from, in the format YYYY-mm-dd.
    Returns:
        A list of dictionaries, each representing a customer visit, with keys: product_id, quantity_ordered, discount_factor, order_status, and date_ordered.
    """

    cols = ["product_id", "quantity_ordered", "discount_factor", "order_status", "date_ordered"]
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
    Specialized Customer Service Agent Tool.
    Get all records of a customer's orders
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
    Returns:
        A list of dictionaries, each representing a customer's order, with keys: product_id, quantity_ordered, discount_factor, order_status, and date_ordered.
    """

    cols = ["product_id", "quantity_ordered", "discount_factor", "order_status", "date_ordered"]
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
    Specialized Customer Service Agent Tool.
    Upload details of a customer's order to the database
    
    Args:
        business_id (str): the id of the business to search for (in string format).
        customer_id (str): the id of the customer in the database.
        product_id (str): the id of the product being ordered.
        quantity_ordered (int): the amount of the product to order.
        discount_factor (float): the percentage of discount being applied to the order (ranging from 0.0 as no discount to 1.0 as 100% discount).
    Returns:
        A response notifying whether or not record upload was successful.
    """

    tbl_name = "customer_order"
    cols = ["customer_id", "business_id", "product_id", "quantity_ordered", "discount_factor", "order_status", "date_ordered"]
    cols = f"({', '.join(cols)})"
    time_of_order = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = (customer_id, business_id, product_id, quantity_ordered, discount_factor, "pending", time_of_order)
    values_fmt = "%s, %s, %s, %s, %s, %s"
    result = insert(tbl_name, cols, values, values_fmt)
    return result


upload_customer_details.__doc__ = f"""
    Specialized Customer Service Agent Tool.
    Uploads details of a customer to the database

    The value of the `name` must be formatted in the following way:
    {params_format()}

    Args:
        id (str): the id of the customer
        business_id (str): the id of the business to which the customer belongs.
        username (str): the telegram username of the customer.
        name (str): the name of the customer.
        age (int): the age of the customer.
        gender (str): the gender of the customer (as M for male or F for female).
        contact_details (str): the phone number or other contact detail of the customer.
    Return:
        A response notifying whether or not record upload was successful
    """

get_specific_product_info.__doc__ = f"""
    Specialized Customer Service Agent Tool.
    Get details of a specific product by searching, either by the product's id, or the name provided.

    The value of the product parameter must be formatted in the following way:
          {params_format()}

    Args:
        business_id (str): the id of the business to search for (in string format).
        (optional) product_id (str): the id of the product to search for. You can choose to pass an empty string for this parameter if no value is available.
        (optional) product_name (str): the name of the product. You can choose to pass an empty string for this parameter if no value is available.
        Note: Either the product_id or product_name must be provided, both cannot be empty.
    Returns:
        A list of dictionaries, each representing a product with matching name/id, with keys: id, item_name, category, brand, quantity_in_stock, selling_price, and minimum_selling_price.
    """

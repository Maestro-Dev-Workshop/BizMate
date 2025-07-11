from database_manager.tools import *
from utils.db_utils import get_rows_with_exact_column_values, insert
import datetime
import os


def get_business_details(
        business_id: str
):

    cols = ["id","username", "name", "business_name"]
    result = get_rows_with_exact_column_values(
        "business", 
        ["id"], 
        [business_id], 
        cols)
    
    if isinstance(result, str):
        return result
    else:
        if result:
            return {cols[i]: result[0][i] for i in range(len(cols))}
        else:
            return "business record not found"

def log(
    id :int
):
    """
    Once called, it logs the business
    Args:

    id(str):business id
    
    Returns whether it was successful or it failed
    """
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return insert("log_history","(business_id, login_time)",(id,dt),"%s, %s")

def get_recent_orders(id):
    cursor.execute("SELECT MAX(login_time) FROM log_history WHERE business_id=%s",(id,))
    last_login = cursor.fetchone()
    last_login = last_login[0]
    cursor.execute("SELECT * FROM customer_order WHERE business_id=%s and TIMESTAMPDIFF(MINUTE, date_ordered, %s) <= 30", (id,last_login))
    return cursor.fetchall()

get_business_details.__doc__ = """
Gets business details

Args:
id : Business id

Returns :
Whether it exists
"""
log.__doc__ = """
Logs Business details

Args:
id: The business id

Returns
Whether operation was successful

"""
get_recent_orders.__doc__ = """
Get the recent order made 
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main.utils.db_utils import *
import datetime


def add_business(
        id : str,
        username : str,
        name : str,
        business_name : str,
        brief_description : str,
        contact_details : str,
        physical_address: str,
        dob:str,
        bot_username: str,
        bot_link: str) -> str:
    dob = datetime.datetime.strptime(dob,"%Y-%m-%d").date()
    date_joined = datetime.date.today()
    values = (id, username, name, business_name, brief_description, date_joined, contact_details,physical_address,dob,True,bot_username, bot_link)
    fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    columns = "(id, username, business_name, brief_description, date_joined, contact_details, physical_address, date_of_birth, active, bot_username, bot_link)"
    return insert("business", columns, values, fmt)

add_business.__doc__ = f"""
Adds a business's basic information to the database.

The values of `name` and `business_name` must be formatted as follows:
{params_format()}

Args:
    id(str) : The business id
    Username (str) : Username of the business admin
    name (str): Name of the business owner.
    business_name (str): Name of the business.
    brief_description (str): Brief description of the business.
    contact_details (str): Email or phone number of the business.
    physical_address (str): The physical location of the business.
    dob (str): Date of birth in YYYY-MM-DD format.
    bot_username (str): Bot Username
    bot_link (str): Bot link

Returns:
    str: Message indicating if the insertion was successful.
"""


def delete_business(business_id : str) ->str:
    return update_table("business",["id"],[business_id],["active"],[False])

def verify_business(business_name: str) -> str:
    ids = get_rows_with_exact_column_values("business", "business_name", business_name, "id"),
    actives = get_rows_with_exact_column_values("business", "business_name", business_name, "active")
    for id, active in zip(ids,actives):
        if isinstance(active[0],int):
            if active:
                return "Exists"
    return "Does Not Exist"

delete_business.__doc__ = f"""Updates active column to false
    Args:
        business_id(str): ID of the business
    
    Returns
        whether the update operation was successful or not
    """

verify_business.__doc__ = f"""Verifies if the business exist then it returns the id
    The values of the  `business_name` must be formatted in the following way:
        {params_format()}
    Args:
        business_name(str): name of the business
    
    Returns:
        the id of the business if it exists
    """
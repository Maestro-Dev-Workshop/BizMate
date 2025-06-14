import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database_manager.tools import *
import datetime


def add_business(
        name : str,
        business_name : str,
        brief_description : str,
        contact_details : str,
        physical_address: str,
        dob:str,
        password:str) -> str:
    f"""Adds a business basic information to the database
    Args:
        name(str): Name of the business owner
        business_name(str): Name of the business
        brief_description(str): Brief description about the database
        contact_details(str): The contact details of the user either email or phone number
        physical_address(str): The physical address of the store
        dob(str): User's date of birth in (YYYY-MM-DD)
        password: User's password
    
    The values of name, business_name must be formatted in the following way:
     {params_format()}
    
    Returns: A message stating whether the operation was successful
    """
    dob = datetime.datetime.strptime(dob,"%Y-%m-%d").date()
    date_joined = datetime.date.today()
    values = (name, business_name, brief_description, date_joined, contact_details,physical_address,dob,password,True,True)
    fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    columns = "(username, business_name, brief_description, date_joined, contact_details, physical_address, date_of_birth, password, active, basic_info)"
    return insert("business", columns, values, fmt)

def delete_business(business_name : str) ->str:
    f"""Updates active column to false
    
    Args:
        business_name(str): Name of the business
    
    The values of the business_name must be formatted in the following way:
     {params_format()}
    Returns
        whether the update operation was successful or not
    """
    return update_table("business",["business_name"],[business_name],["active"],[False])

def verify_business(business_name: str) -> str:
    f"""Verifies if the business exist then it returns the id
    
    Args:
        business_name(str): name of the business
    
    The values of the business_name must be formatted in the following way:
     {params_format()}
    
    Returns:
        the id of the business if it exists
    """
    ids = get_rows_with_exact_column_values("business", "business_name", business_name, "id"),
    actives = get_rows_with_exact_column_values("business", "business_name", business_name, "active")
    for id, active in zip(ids,actives):
        if isinstance(active[0],int):
            if active:
                return "Exists"
    return "Does Not Exist"

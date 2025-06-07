import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','..')))
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
    """Adds a business basic information to the database
    Args:
        name(str): Name of the business owner
        business_name(str): Name of the business
        brief_description(str): Brief description about the database
        contact_details(str): The contact details of the user either email or phone number
        physical_address(str): The physical address of the store
        dob(str): User's date of birth in (YYYY-MM-DD)
        password: User's password
    
    Returns: A message stating whether the operation was successful
    """
    dob = datetime.datetime.strptime(dob,"%Y-%m-%d").date()
    date_joined = datetime.date.today()
    values = (name, business_name, brief_description, date_joined, contact_details,physical_address,dob,password,True,True)
    fmt = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    columns = "(username, business_name, brief_description, date_joined, contact_details, physical_address, date_of_birth, password, active, basic_info)"
    return insert("business", columns, values, fmt)


# print(add_business(
#     name="Quam",
#     business_name="GS",
#     brief_description="evoerv,se",
#     contact_details="evorev",
#     physical_address="evmepw,",
#     dob="2005-04-01",
#     password="everv"
# ))

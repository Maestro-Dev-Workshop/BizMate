from db_utils import db, cursor
from datetime import datetime
from database_manager.tools import insert, get_single_value, update_table

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
    
    Returns: A message stating whether the operation was successfull
    """
    dob = datetime.strptime(dob,"%Y-%m-%d").date()
    date_joined = datetime.date.today()
    values = (name, business_name, brief_description, date_joined, contact_details,physical_address,dob,password,True)
    fmt = "%s, %s, %s, %s, %s, %s, %s, %s"
    columns = "(username, business_name, brief_description, date_joined, contact_details, physical_address, dob(str), password, active)"
    return insert("business", columns, values, fmt)


def add_product(
        business_name:str,
        item_names:list[str],
        manufacturers:list[list[str]],
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
    cols = (manufacturers, quantities, sps, negotiate_percents, expiry_dates, metadata)
    expiry_dates = [[datetime.strptime(exp, "%Y-%m-%d").date() for exp in sublist] for sublist in expiry_dates]
    columns = "(business_id, item_name, manufacturer, quantity_in_stock, selling_price, negotiate_percent, expiry_date, metadata)"
    fmt = fmt = "%s, %s, %s, %s, %s, %s, %s, %s"
    message = {}
    for ind in range(len(item_names)):
        for sub_ind in range(len(manufacturers[ind])):
            row = [business_id, item_names[ind]] + [col[ind][sub_ind] for col in cols]
            message[f"{item_names[ind]}, Manufacturer: {manufacturers[ind][sub_ind]}"] = insert("product", columns, row, fmt)
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
    for ind, product in enumerate(product_ids):
        supplier_vals = (business_id,name, contact_det)
        message[f"supplier:{name}"] = insert("supplier", supplier_cols, supplier_vals, supp_fmt)
        cursor.execute("""SELECT id from supplier WHERE business_id=%s AND contact_details=%s""",(business_id,contact_det))
        supplier_id = cursor.fetchone()[0]
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
    return update_table("business","business_name",business_name,"active",False)

def verify_business(business_name: str) -> str:
    """Verifies if the business exist then it returns the id
    
    Args:
        business_name(str): name of the business
    
    Returns:
        the id of the business if it exists
    """
    id = get_single_value("business", "business_name", business_name, "id"),
    active = get_single_value("business", "business_name", business_name, "active")
    if isinstance(active,bool):
        return id if active else "Does not Exist"
    else:
        return id

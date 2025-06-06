from db_utils import db, cursor
from datetime import datetime
# tools
# business manager
# create a 
    # business
    # product
    # supplier
#Modify  business details
# delete a business
# verify business

# username, business_name, brief_description, date_joined, contact_details, physical_address, date_of_birth, password
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
    values = (name, business_name, brief_description, date_joined, contact_details,physical_address,dob,password)
    fmt = "%s, %s, %s, %s, %s, %s, %s"
    columns = "(username, business_name, brief_description, date_joined, contact_details, physical_address, dob(str), password)"
    return insert("business", columns, values, fmt)

def insert(
        tblname :str,
        cols : str,
        values : tuple|list,
        values_fmt : str):
    """General function to insert row into table
    
    Args:
        tblname : name of table for row to be inserted to
        cols : name of the columns
        values : the values of the columns
        values_fmt : format of the values

    Returns:
        Whether the row insertion was successful
    """
    query = f"""INSERT INTO {tblname} ({cols}) VALUES ({values_fmt})"""
    try:
        cursor.execute(query, values)
        return "Row inserted"
    except Exception as e:
        db.rollback()
        return f"Error adding row: {e}"


def get_single_value(
    tbl_name : str,
    col_name : str,
    value : str,
    target_col : str
    ):
    """Returns a single result result of a query
    Args:
        tbl_name: name of the table,
        col_name: name of the column to filter from
        value : the value of the column
        target_col : from which column should the result come from
    
    Returns:
        the result of the query
    """
    query = f"SELECT {target_col} FROM {tbl_name} WHERE {col_name} = %s"
    try:
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        return f"Error: {e}"


# business_name, item_name, quantity, producer, quantity_in_stock, selling_price, negotiate-percent, expiry_date, metadata
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

# business_name, supplier_name, contact_details, products, cost_prices, metadata, manufacturer ,available
def add_supplier(business_name:str,
                name:list[str],
                contact_det: str, 
                products: list[str],
                cost_prices: list[list[str]],
                metadatas: list[list[str]],
                manufacturer: list[list[str]],
                available:list[list[str]]):
    pass
    

#business_name, table_name ,column_name , new_value
def modify_business():
    pass

# business_name
def delete_business():
    pass

# business_name
def verify_business():
    pass

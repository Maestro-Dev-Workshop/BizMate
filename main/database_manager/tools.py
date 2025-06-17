from .db_utils import db, cursor
import datetime
from decimal import Decimal

def serialize_dict(obj):
    if isinstance(obj, dict):
        return {k: serialize_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_dict(i) for i in obj]
    elif isinstance(obj, tuple):
        return [serialize_dict(i) for i in obj]
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def list_tables() -> list[str]:
    """Retrieve the names of all tables in the database."""

    try:
        cursor.execute("SHOW TABLES")
        tables = [tbl[0] for tbl in cursor.fetchall()]
        return tables
    except Exception as e:
        return f"Error: {e}"

def describe_table(table_name: str) -> list[tuple[str, str]]:
    """
    Look up the table schema.

    Args:
        table_name: the name of the table to describe
    Returns:
        List of columns, where each entry is a tuple of the format (column name, data_type, null (if it can be NULL), key (e.g., PRI for primary key), default value, extra info).
    """

    try:
        cursor.execute(f"DESCRIBE {table_name}")
        schema = cursor.fetchall()
        return schema
    except Exception as e:
        return f"Error: {e}"

def execute_query(sql: str) -> list[list[str]]:
    try:
        cursor.execute(sql)
        return serialize_dict(cursor.fetchall())
    except Exception as e:
        return f"Error: {e}"

def execute_query_in_str(sql: str) -> list[list[str]]:
    """
    General function to execute an SQL statement, returning the results. Can be used to extract useful information.
    
    Args:
        sql: the query to be executed
    Returns:
        The result of the query
    """

    try:
        cursor.execute(sql)
        return f"""{cursor.fetchall()}"""
    except Exception as e:
        return f"Error: {e}"

def params_format():
    return """
    - All letters should be lowercase.
    - Remove any leading or trailing whitespace.
    - Replace any spaces between words with underscores (_).
    - For product_name or item_name parameters, convert plural words to their singular form.
    - For product_name or item_name parameters, do not include any descriptive text, for example granola_bar_(chocolate) -> granola_bar, add the description to the metadata parameter
    """

# Quam oni werey
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
    query = f"""INSERT INTO {tblname} {cols} VALUES ({values_fmt})"""
    try:
        cursor.execute(query, values)
        db.commit()
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

    query = f"SELECT {target_col} FROM {tbl_name} WHERE {col_name} = %s"
    try:
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        cursor.reset()
        return result[0] if result else None
    except Exception as e:
        return f"Error: {e}"

def get_rows_with_exact_column_values(
    tbl_name: str,
    col_names: list[str],
    values: list[str],
    target_cols: list[str]
    ):

    filters = []
    for i in range(len(col_names)):
        filters.append(f"{col_names[i]} = %s")
    query = f"SELECT {', '.join(target_cols)} FROM {tbl_name} WHERE {' AND '.join(filters)}"
    
    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
        return serialize_dict(result)
    except Exception as e:
        return f"Error: {e}"

def get_rows_with_matching_column_values(
    tbl_name: str,
    col_names: list[str],
    values: list[str],
    target_cols: list[str]
    ):

    filters = []
    for i in range(len(col_names)):
        filters.append(f"{col_names[i]} LIKE %s")
    query = f"SELECT {', '.join(target_cols)} FROM {tbl_name} WHERE {' AND '.join(filters)}"
    values = [f"%{value}%" for value in values]

    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
        return serialize_dict(result)
    except Exception as e:
        return f"Error: {e}"

def update_table(tbl_name : str,
                col_names : list[str],
                col_vals : list[str],
                target_cols : list[str],
                target_vals : list[str]) -> str:
    filters = " AND ".join([f"{col} = %s" for col in col_names])
    targets = ", ".join([f"{col} = %s" for col in target_cols])
    query = f"""UPDATE {tbl_name} SET """ + targets + " WHERE " + filters
    try:
        cursor.execute(query, target_vals + col_vals)
        db.commit()
        return "Updated"
    except Exception as e:
        db.rollback()
        return f"Error updating {tbl_name}: {e}"

def delete_row(tbl_name : str,
                col_names : list[str],
                col_vals : list[str]):
    filters = " AND ".join([f"{col} = %s" for col in col_names])
    query = f"""DELETE FROM {tbl_name} WHERE """ + filters
    try:
        cursor.execute(query, col_vals)
        db.commit()
        return "Deleted"
    except Exception as e:
        db.rollback()
        return f"Error deleting from {tbl_name}: {e}"

def login(business_name :str,
                    password : str) -> str:

    query = """SELECT id,username, business_name, brief_description, contact_details, physical_address FROM business WHERE business_name=%s and password=%s and active=1"""
    cursor.execute(query, (business_name, password))
    detail = cursor.fetchall()
    if len(detail) == 0:
        return "Invalid Details"
    else:
        return detail[0]


execute_query.__doc__ = f"""
    General function to execute an SQL statement, returning the results. Can be used to extract useful information.
    
    If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:
        {params_format()}
    Args:
        sql: the query to be executed
    Returns:
        The result of the query
    """

get_single_value.__doc__ = f"""
    Returns a single result result of a query

    If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:
        {params_format()}

    Args:
        tbl_name: name of the table,
        col_name: name of the column to filter from
        value : the value of the column
        target_col : from which column should the result come from
    
    Returns:
        the result of the query
    """

get_rows_with_exact_column_values.__doc__ = f"""
    Filters records by rows whose values exactly match the provided value in the specified column 
    
    If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:
        {params_format()}

    Args:
        tbl_name (str): name of the table
        col_names (list[str]): names of the columns to filter from
        value (list[str| int |float]): the values to filter by
        target_cols (list[str]): list of columns to show
        Note: The number of elements in col_names must match that of values
    
    Returns:
        Rows that fulfill the stated condition
    """

get_rows_with_matching_column_values.__doc__ = f"""
    Filters records by rows whose values having matching pattern to the provided values in the specified columns. Can be used as a searching function

        If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:

        {params_format()}

    Args:
        tbl_name: name of the table
        col_names: names of the columns to filter from
        value: the values to filter by
        target_cols: list of columns to show
        Note: The number of elements in col_names must match that of values
    
    Returns:
        Rows that fulfill the stated condition
    """

update_table.__doc__ = f"""
    General function for updating tables

        If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:

        {params_format()}

    Args:
        tbl_name(str): Name of the table to update
        col_names(list[str]): List of columns to be filtered
        col_vals(list[str]): Contains values of the columns selected to be filtered
        target_cols(list[str]): List of columns to be updated
        target_vals(list[str]): contains the updated values for the targeted columns
    Returns:
        whether the update operation was successful
    """

delete_row.__doc__ = f"""
    General function for deleting rows from table

        If you're dealing with names or item names or similar columns except passwords or contact detail, ensure their values are formatted as:

        {params_format()}

    Args:
        tbl_name(str): Name of the table to update
        col_names(list[str]): List of columns to be filtered
        col_vals(list[str]): Contains values of the columns selected to be filtered
    Returns:
        whether the delete operation was successful
    """

login.__doc__ = f"""
    Verifies the details
    
    Ensure the business_name is formatted in the following way:
    {params_format()}

    Args:

    business_name(str) : Name of the business
    password(str) : Password

    Returns: 
    whether the detail exist
    """

from db_utils import db, cursor
from datetime import datetime

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
        return [(col[1], col[2]) for col in schema]
    except Exception as e:
        return f"Error: {e}"

def execute_query(sql: str) -> list[list[str]]:
    """
    General function to execute an SQL statement, returning the results. Can be used to extract useful information.
    
    Args:
        sql: the query to be executed
    Returns:
        The result of the query
    """

    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        return f"Error: {e}"

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

def get_rows_with_exact_column_value(
    tbl_name: str,
    col_name: str,
    value: str
    ):
    """
    Filters records by rows whose values exactly match the provided value in the specified column 
    
    Args:
        tbl_name: name of the table
        col_name: name of the column to filter from
        value: the value to filter by
    
    Returns:
        Rows that fulfill the stated condition
    """

    query = f"SELECT * FROM {tbl_name} WHERE {col_name} = %s"
    try:
        cursor.execute(query, (value,))
        result = cursor.fetchall()
        return result[0] if result else None
    except Exception as e:
        return f"Error: {e}"

def get_rows_with_matching_column_value(
    tbl_name: str,
    col_name: str,
    value: str
    ):
    """
    Filters records by rows whose values having matching pattern to the provided value in the specified column. Can be used as a searching function
    
    Args:
        tbl_name: name of the table
        col_name: name of the column to filter from
        value: the value to filter by
    
    Returns:
        Rows that fulfill the stated condition
    """

    query = f"SELECT * FROM {tbl_name} WHERE {col_name} = %%s%"
    try:
        cursor.execute(query, (value,))
        result = cursor.fetchall()
        return result[0] if result else None
    except Exception as e:
        return f"Error: {e}"

def update_table(tbl_name : str,
                col_names : list[str],
                col_vals : list[str],
                target_cols : list[str],
                target_vals : list[str]) -> str:
    """
    General function for updating tables

    Args:
        tbl_name(str): Name of the table to update
        col_names(list[str]): List of columns to be filtered
        col_vals(list[str]): Contains values of the columns selected to be filtered
        target_cols(list[str]): List of columns to be updated
        target_vals(list[str]): contains the updated values for the targeted columns
    Returns:
        whether the update operation was successful
    """
    filters = " AND ".join([f"{col} = %s" for col in col_names])
    targets = ", ".join([f"{col} = %s" for col in target_cols])
    query = f"""UPDATE {tbl_name} SET """ + targets + "WHERE" + filters
    try:
        cursor.execute(query, target_vals + col_vals)
        return "Updated"
    except Exception as e:
        db.rollback()
        return f"Error updating {tbl_name}: {e}"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main.utils.db_utils import *
import datetime

def draft_select_query(
    table_name: str,
    columns: str,
    where_clause: str,
    group_by: str,
    order_by: str,
    limit: str,
    join_table: str,
    join_type: str,
    join_column: str,
    ):
  """
  Generates a SQL query to select data from a table.

  Args:
    table_name: The name of the table (or view) to select from.
    columns: The columns to select. Use '*' to select all columns. If aggregations are to be done (e.g MIN, MAX, SUM, e.t.c), they should be added in this argument. Operations could also be added here to generate new columns.
    where_clause: The WHERE clause to apply to the query. Use 'None' to omit the WHERE clause.
    group_by: The column(s) to group by. Use 'None' to omit the GROUP BY clause.
    order_by: The column to order by. Use 'None' to omit the ORDER BY clause.
    order_type: The type of order to perform (e.g ASC or DESC). Always use only use if and only if join_table specified.
    limit: The number of rows to select. Use 'None' to omit the LIMIT clause.
    join_table: The table to join with. Use 'None' to omit the JOIN clause.
    join_type: The type of join to perform (Allowable values are 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'CROSS JOIN'). Always use only use if and only if join_table specified.
    join_column: The column to join on. Always use only use if and only if join_table specified.
  Returns:
    The generated query as a string.
  """
  print(f" - DB CALL: draft_select_query({table_name}, {columns}, {where_clause}, {group_by}, {order_by}, {limit}, {join_table}, {join_type}, {join_column})")

  query = f"SELECT {columns} FROM {table_name}"
  if join_table:
    query += f" {join_type} JOIN {join_table} ON {table_name}.{join_column} = {join_table}.{join_column}"
  if where_clause:
    query += f" WHERE {where_clause}"
  if group_by:
    query += f" GROUP BY {group_by}"
  if order_by:
    query += f" ORDER BY {order_by}"
  return query

def draft_temp_view_query(view_name: str, select_query: str):
  """
  Generates a SQL query to create a temporary view.

  Args:
    view_name: The name of the view to create.
    select_query: The SELECT query to use to create the view.
  Returns:
    The generated query as a string.
  """
  print(f" - DB CALL: draft_temp_view_query({view_name}, {select_query})")

  return f"CREATE TEMP VIEW {view_name} AS {select_query}"

def get_schema_for_all_tables():
  """
  Retrieves the schema for all the tables in the database

  Returns:
    A dictionary mapping table names to their schema.
  """
  print(f" - DB CALL: get_schema_for_all_tables()")

  tables = list_tables()
  schemas = {}
  for table in tables:
    schemas[table] = describe_table(table)
  return schemas
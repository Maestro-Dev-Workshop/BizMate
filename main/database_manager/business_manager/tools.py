import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from database_manager.db_utils import db, cursor
from database_manager.tools import *
import datetime





# print(add_supplier(
#         "GS",
#         name="SG",
#         contact_det="0402345453",
#         product_ids=["1","2","3","4"],
#         cost_prices=[10000,5000,2300,1000],
#         available=[True,False,False,True]
#     )
# )

# print(verify_business("GS"))
# print(verify_business("rveim"))
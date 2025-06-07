import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from database_manager.db_utils import db, cursor
from database_manager.tools import *
import datetime





# print(
#     add_product(
#         "GS",
#         item_names=["Cement", "Vegetable Oil"],
#         brands=[["Dangote", "Lafarge"],["King", "Mamador"]],
#         quantities=[[200,20],[10,5]],
#         sps=[[11000,14000],[4000,2000]],
#         negotiate_percents=[[0,0],[3,2]],
#         expiry_dates=[["2030-03-04","2036-04-05"],["2026-03-30","2025-02-20"]],
#         metadata=[["10kg","In half bags"], ["20kg","2kg"]]
#     )
# )

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
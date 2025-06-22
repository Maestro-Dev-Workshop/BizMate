from main.utils.db_utils import db, cursor

def get_contact_details(business_id:str):
    cursor.execute("""SELECT tg_bot_username FROM business WHERE id=%s""",(business_id,))
    username = cursor.fetchone()
    cursor.reset()
    return username

get_contact_details.__doc__ = f"""
Gets the customer service contact details of a business

Args:
business_id(str) : The id of the business

Returns:
the customer service details

"""
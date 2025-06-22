import mysql.connector
from dotenv import load_dotenv
import os
from googleapiclient import discovery
from google.auth import default
from urllib.parse import quote_plus
load_dotenv()

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

IP = '34.135.212.39'

hosted = {
    "host":IP,
    "user":USER,
    "password":PASSWORD,
    "database":"bizdb"
}

db = mysql.connector.connect(**hosted)
DB_URL = f"mysql+pymysql://{USER}:{quote_plus(PASSWORD)}@{IP}:3306/bizmate_session_service"
cursor = db.cursor()
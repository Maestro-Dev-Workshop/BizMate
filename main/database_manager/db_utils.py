import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

# hosted
hosted = {
    "host":"34.57.91.175",
    "user":"dbuser",
    "password":"Root@1234",
    "database":"bizdb"
}

# Local
local = {
    "host":"localhost",
    "user":"root",
    "password":"root",
    "database":"bizdb"
}

db = mysql.connector.connect(**local)
cursor =db.cursor()
# cursor = db.cursor()
# cursor.execute("SHOW DATABASES")


# CREATE USER 'dbuser'@'102.88.114.17' IDENTIFIED BY 'Root@1234';
# GRANT ALL PRIVILEGES ON *.* TO 'dbuser'@'102.88.114.17';
# FLUSH PRIVILEGES;
# Issues
# 1. Trigger to start and stop the compute instance
# 2. IP address of the compute instance changes
# 3. Local IP address also changes
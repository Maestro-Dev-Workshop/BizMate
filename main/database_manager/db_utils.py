import mysql.connector
from dotenv import load_dotenv
import os
from googleapiclient import discovery
from google.auth import default
load_dotenv()

def get_instance_external_ip(project_id, zone, instance_name):
    credentials, _ = default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    request = service.instances().get(project=project_id, zone=zone, instance=instance_name)
    response = request.execute()

    # Extract external IP
    interfaces = response['networkInterfaces']
    access_configs = interfaces[0].get('accessConfigs', [])
    
    if access_configs:
        return access_configs[0].get('natIP')
    else:
        return None

PROJECT_ID=os.environ["PROJECT_ID"]
ZONE=os.environ["ZONE"]
INSTANCE=os.environ["INSTANCE"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

IP = get_instance_external_ip(PROJECT_ID, ZONE, INSTANCE)

hosted = {
    "host":IP,
    "user":USER,
    "password":PASSWORD,
    "database":"bizdb"
}

db = mysql.connector.connect(**hosted)
cursor = db.cursor()
# CREATE USER 'dbuser'@'%' IDENTIFIED BY 'bizMate@v0';
# GRANT ALL PRIVILEGES ON *.* TO 'dbuser'@'%';
# FLUSH PRIVILEGES;

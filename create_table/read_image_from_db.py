import pymssql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

# Connection parameters for SQL Server
server = 'moneysave.softether.net'
port = 1433
database = 'chatbot2'
username = 'ChatBot'
password = 'MoneySave+123'

# Connect to SQL Server
connection = pymssql.connect(server, username, password, database)

# Query to retrieve image data
query = "SELECT TOP 1 ImageData FROM Images"  # Assuming the table is named Images
with connection.cursor() as cursor:
    cursor.execute(query)
    image_data = cursor.fetchone()[0]

# Close SQL connection
connection.close()

# Save image data as a file
image_path = 'image_from_sql.png'
with open(image_path, 'wb') as file:
    file.write(image_data)

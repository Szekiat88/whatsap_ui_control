import pymssql

# Connection parameters
server = 'moneysave.softether.net'
port = 1433
database = 'chatbot2'
username = 'ChatBot'
password = 'MoneySave+123'

# Connect to SQL Server
connection = pymssql.connect(server, username, password, database)

# Read the image file
with open('C:\\Users\\ChanMengKwan\\Documents\\GitHub\\whatsap_ui_control\\googlechromeversion.png', 'rb') as file:
    image_data = file.read()
    print(image_data)

# Insert image data into the database
with connection.cursor() as cursor:
    cursor.execute("INSERT INTO Images (ImageData) VALUES (%s)", (image_data,))
    connection.commit()

# Close connection
connection.close()

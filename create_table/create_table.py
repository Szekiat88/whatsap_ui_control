import pymssql

# Connection parameters
server = 'moneysave.softether.net'
port = 1433
database = 'chatbot2'
username = 'ChatBot'
password = 'MoneySave+123'


def connect_to_database():
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    return conn, cursor

def commit_changes(connection):
    connection.commit()
    
def close_connection(cursor, connection):
    cursor.close()
    connection.close()

def create_customer_info(cursor,connection):
    insert_query = '''
    CREATE TABLE prospect_personal_info (
        id INT IDENTITY(1,1) PRIMARY KEY,
        client_name NVARCHAR(100),
        phone_number VARCHAR(20),
        email VARCHAR(100),
        age INT,
        birthday DATE,
        sex VARCHAR(10),
        job VARCHAR(100),
        working_area VARCHAR(100),
        looking_area VARCHAR(100),
        budget DECIMAL(10,2),
        required_rooms INT,
        num_children INT,
        purpose VARCHAR(1000),
        staying_area VARCHAR(100),
        marital_status VARCHAR(20),
        created_date DATETIME DEFAULT GETDATE(),
        modified_date DATETIME DEFAULT GETDATE(),
        country_code VARCHAR(2),
        is_duplicate INT,
        is_contact_created_in_google BIT,
        data_source VARCHAR(50)
        );  
        '''
    cursor.execute(insert_query)
    commit_changes(connection)


connection, cursor = connect_to_database()
hello = create_customer_info(cursor,connection)

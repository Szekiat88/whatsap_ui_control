import pymssql
import re
import client_data as cd

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

def insert_customer_data(cursor, connection, user_data):
    insert_query = '''
        INSERT INTO [prospect_personal_info] (client_name, phone_number, country_code, is_duplicate)
        VALUES (%s, %s, %s, %s);
        '''

    for data in user_data:
        contact_number = data['contact_number']

        # Skip records with less than 6 numbers in contact_number
        if len(contact_number) < 6:
            continue

        if contact_number.startswith('1') or contact_number.startswith('01'):
            contact_number = '601' + contact_number[1:]
            country_code = 'MY'
        elif contact_number.startswith('6001'):
            contact_number = '601' + contact_number[4:]
            country_code = 'MY'
        elif contact_number.startswith('65'):
            country_code = 'SG'
        elif contact_number.startswith('6665') or contact_number.startswith('665'):
            contact_number = '65' + contact_number[3:]
            country_code = 'SG'
        else:
            country_code = 'MY'

        cursor.execute("SELECT COUNT(*) FROM [prospect_personal_info] WHERE phone_number = %s", (contact_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("UPDATE [prospect_personal_info] SET is_duplicate = is_duplicate + 1 WHERE phone_number = %s", (contact_number,))
        else:
            cursor.execute(insert_query, (data['name'], contact_number, country_code, 1))

    commit_changes(connection)

pattern = re.compile(r'(.+?)\s+(\d+)')

matches = pattern.findall(cd.data)
user_data = [{'name': match[0], 'contact_number': match[1]} for match in matches]

connection, cursor = connect_to_database()
insert_customer_data(cursor, connection, user_data)

close_connection(cursor, connection)

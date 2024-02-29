from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pymssql

SCOPES = ['https://www.googleapis.com/auth/contacts']

def connect_to_database():
    server = 'moneysave.softether.net'
    port = 1433
    database = 'chatbot2'
    username = 'ChatBot'
    password = 'MoneySave+123'
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    return conn, cursor

def retrieve_contacts_to_create(cursor):
    cursor.execute("SELECT id,client_name,phone_number,country_code FROM [prospect_personal_info] WHERE is_contact_created_in_google is NULL")
    return cursor.fetchall()

def update_contact_status(cursor, contact_id):
    cursor.execute("UPDATE [prospect_personal_info] SET is_contact_created_in_google = '0', data_source ='fan da leads' WHERE id = %s", (contact_id,))
    cursor.connection.commit()  # Use cursor.connection.commit() instead of cursor.commit()

def generate_custom_name(client_id, client_name, country_code):
    return f"C{client_id}_{client_name}_{country_code}"

def create_google_contact(service, contact_data):
    service.people().createContact(body=contact_data).execute()

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    connection, cursor = connect_to_database()

    contacts_to_create = retrieve_contacts_to_create(cursor)

    for contact in contacts_to_create:
        contact_data = {
            "names": [{"givenName": generate_custom_name(contact[0], contact[1], contact[3])}],
            "phoneNumbers": [{"value": contact[2]}],
        }

        create_google_contact(service, contact_data)

        contact_id = contact[0]
        update_contact_status(cursor, contact_id)

    # Close the database connection
    connection.close()

if __name__ == '__main__':
    main()

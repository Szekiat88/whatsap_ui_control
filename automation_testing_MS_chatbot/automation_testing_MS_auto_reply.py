from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.webdriver.common.keys import Keys


import pymssql

# Connection parameters
server = 'moneysave.softether.net'
port = 1433
database = 'chatbot'
username = 'ChatBot'
password = 'MoneySave+123'
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0, api_key="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")



def connect_to_database():
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    return conn, cursor

def commit_changes(connection):
    connection.commit()

def find_article_general_knowledge(cursor,article_id):
    select_all_query = '''
        SELECT [question]
        FROM article_general_knowledge
        where [article_id] = %s;
    '''
    cursor.execute(select_all_query,(article_id,))
    return cursor.fetchall()

def insert_generated_testing_question_tracking(cursor,connection,question,ori_question,template_id):
    insert_query = '''
        INSERT INTO generated_testing_question_tracking (question,ori_question,template_id)
        VALUES (%s,%s,%s);    
        '''
    cursor.execute(insert_query, (question,ori_question,template_id,))
    commit_changes(connection)

options=webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/szekiatpua/AppData/Local/Google/Chrome/User Data")

driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win32\\chromedriver.exe', chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait=WebDriverWait(driver,100)
driver.maximize_window()


new_chat_button_xpath = '//div[@title="New chat"]'
new_chat_button = wait.until(EC.element_to_be_clickable((By.XPATH, new_chat_button_xpath)))
new_chat_button.click()

driver.switch_to.active_element.send_keys("Moneysave Testing")
time.sleep(1)

driver.switch_to.active_element.send_keys(Keys.ENTER)


conn, cursor=connect_to_database()
for i in range(3, 50):
    article_id = f'A{i}'
    results = find_article_general_knowledge(cursor, article_id)
    print(f"Article ID: {article_id}")
    print(f"SK1: {results}")
    for result in results:
        print(result[0])  #
        messages = [
            SystemMessage(
                content="""You are a Peer-to-peer crowdfunding company who wanted to develop a rule-based chatbot. Currently we are lacking of 
                humanized questions in our knowledgebase. You need to help to generate 5 relevant similar questions based on given question which is more humanized 
                and conversational in Asian style. The returned answer must be in numberic form. """
            ),
            HumanMessage(
                content=result[0]
            ),
        ]

        llm_answer = chat.invoke(messages).content

        questions = re.split(r'\d+\.', llm_answer)

        for question in questions:
            question = question.strip()
            if question:
                insert_generated_testing_question_tracking(cursor=cursor,connection=conn,question=question,ori_question=result[0],template_id='1_winson')
                print(question)
                # Locate the message input textbox
                # can comment for avoiding message sending 
                message_input_xpath = '//div[@title="Type a message"]'
                message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
                
                message_input.send_keys(question)

                wait=WebDriverWait(driver,10000)
                time.sleep(3)
                send_button_xpath = "//span[@data-icon='send']"
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
                send_button.click()
                time.sleep(180)
                #till here







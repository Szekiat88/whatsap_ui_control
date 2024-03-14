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
password = 'ChatBot+123'
import re
import google.generativeai as genai

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0, api_key="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")
genai.configure(api_key='AIzaSyB6twsitxlr0q1cbVUaYQf5BToyM_Czjm8')
model = genai.GenerativeModel('models/gemini-pro')

config = {"max_output_tokens": 2048, "temperature": 0.4, "top_p": 1, "top_k": 32}

# Safety config
safety_config =  [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
]



def connect_to_database():
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    return conn, cursor

def commit_changes(connection):
    connection.commit()

def find_article_general_knowledge_by_id(cursor,article_id):
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

def find_article_general_knowledge(cursor):
    select_all_query = '''
        SELECT [article_id], [question]
        FROM article_general_knowledge agk;
    '''
    cursor.execute(select_all_query,)
    return cursor.fetchall()

def get_article_general_knowledge_by_article_id(cursor,article_id):
    select_all_query = '''
        SELECT [article]
        FROM [chatbot].[dbo].[article_general_knowledge]
        where [article_id] = %s; 
    '''
    cursor.execute(select_all_query,(article_id,))
    return cursor.fetchall()

import time

# Define a function to generate content with retry mechanism
def generate_content_with_retry(contents):
    while True:
        try:
            # Attempt to generate content
            responses = model.generate_content(
                contents=contents,
                safety_settings=safety_config,
            )
            # If successful, return responses
            return responses
        except Exception as e:
            print("Error:", e)
            print("Retrying in 5 minutes...")
            time.sleep(300)  # 300 seconds = 5 minutes

# Call the function to generate content with retry
def insert_conversation_history_of_general_knowledge(cursor,connection,user_message,llm_replied_message,article_id):
    insert_query = '''
        INSERT INTO conversation_history_of_general_knowledge (user_message,llm_replied_message,article_id)
        VALUES (%s,%s,%s);    
        '''
    cursor.execute(insert_query, (user_message,llm_replied_message,article_id))
    commit_changes(connection)


def semantic_search_general_knowledge(message, cursor):
    hi = find_article_general_knowledge(cursor)

    formatted_sentences = [f"Sentence - {sentence_id} = {sentence}" for sentence_id, sentence in hi]
    knowledge_base = '\n'.join(formatted_sentences)
    sample_prompt = f"""You are a AI to find the similarity between the question and sentence.
    You need to find the similarity of {message} and {knowledge_base}, then return the full id of the sentence which always 
    started with A, for example A1.
     """
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # responses = model.generate_content(
        #     contents=sample_prompt.format(knowledge_base=knowledge_base, message=message),
        #     safety_settings=safety_config,
        # )
        contents=sample_prompt.format(knowledge_base=knowledge_base, message=message),
        responses = generate_content_with_retry(contents)


        article_id = responses.text
        if article_id.startswith('A'):
            article = get_article_general_knowledge_by_article_id(cursor, article_id)
            answer = article[0][0]
            break  # Break out of the loop if the result starts with 'A'
        else:
            print(f"Attempt {attempts + 1}: Result does not start with 'A'. Retrying...")
            attempts += 1

    if attempts == max_attempts:
        print("Maximum attempts reached. Returning 'I don't know'.")
        answer = "I don't know"
        article_id = None

    return answer, article_id

# options=webdriver.ChromeOptions()
# options.add_argument("user-data-dir=C:/Users/szekiatpua/AppData/Local/Google/Chrome/User Data")

# driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win32\\chromedriver.exe', chrome_options=options)
# driver.get("https://web.whatsapp.com/")
# wait=WebDriverWait(driver,100)
# driver.maximize_window()


# new_chat_button_xpath = '//div[@title="New chat"]'
# new_chat_button = wait.until(EC.element_to_be_clickable((By.XPATH, new_chat_button_xpath)))
# new_chat_button.click()

# driver.switch_to.active_element.send_keys("Moneysave Testing")
# time.sleep(1)

# driver.switch_to.active_element.send_keys(Keys.ENTER)


conn, cursor=connect_to_database()
for i in range(50, 100):
    article_id = f'A{i}'
    results = find_article_general_knowledge_by_id(cursor, article_id)
    print(f"Article ID: {article_id}")
    print(f"SK1: {results}")
    for result in results:
        print(result[0])  #
        messages = [
            SystemMessage(
                content="""You are a Peer-to-peer crowdfunding company who wanted to develop a rule-based chatbot. Currently we are lacking of 
                humanized questions in our knowledgebase. You need to help to generate 5 relevant similar questions based on given question which is more humanized 
                and conversational in Asian style. The returned questions must present in numberic form. """
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
                llm_message, article_id = semantic_search_general_knowledge(question,cursor)
                insert_conversation_history_of_general_knowledge(cursor, conn, question, llm_message, article_id)        

                # Locate the message input textbox
                # can comment for avoiding message sending 
                # message_input_xpath = '//div[@title="Type a message"]'
                # message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
                
                # message_input.send_keys(question)

                # wait=WebDriverWait(driver,10000)
                # time.sleep(3)
                # send_button_xpath = "//span[@data-icon='send']"
                # send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
                # send_button.click()
                # time.sleep(180)
                #till here







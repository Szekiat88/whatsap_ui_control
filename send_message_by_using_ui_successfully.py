from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


import pymssql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import shutil
from selenium.common.exceptions import TimeoutException
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


# driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Documents\\ChromeDriver\\chromedriver_win32\\chromedriver.exe')
options=webdriver.ChromeOptions()

options.add_argument("user-data-dir=C:/Users/szekiatpua/AppData/Local/Google/Chrome/User Data")

driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win32\\chromedriver.exe', chrome_options=options)

#driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win64 (2)\\chromedriver-win64\\chromedriver.exe',chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait=WebDriverWait(driver,100)
driver.maximize_window()
target='"Your Target"'
message="Your Message"
number_of_times=10 #No. of times to send a message


new_chat_button_xpath = '//div[@title="New chat"]'
new_chat_button = wait.until(EC.element_to_be_clickable((By.XPATH, new_chat_button_xpath)))
new_chat_button.click()

# search_start_chat_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Chat list']/div[2]/span[@data-icon='search']")))
# # Click on the chat list button
# search_start_chat_button.click()

# search_start_chat_button.send_keys("jesss jess") 

# driver.switch_to.active_element.send_keys("Hello World")
driver.switch_to.active_element.send_keys("jesss jess")
# Add a delay of 1 second
time.sleep(1)

# Hit Enter
driver.switch_to.active_element.send_keys(Keys.ENTER)

# Locate the message input textbox
message_input_xpath = '//div[@title="Type a message"]'
message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))

#IPPORATMT
#//button[@aria-label='Search or start new chat']/div[2]//span[@data-icon='search']
# Perform actions on the message input textbox
# message_input.send_keys("Your message")  # Replace "Your message" with the text you want to send
# message_input.send_keys("C:/Users/szekiatpua/Documents/GitHub/whatsap_ui_control_y/googlechromeversion.png") 
source_image_path='C:/Users/szekiatpua/Documents/GitHub/whatsap_ui_control_y/googlechromeversion.png'
temp_image_path='C:/Users/szekiatpua/Documents/GitHub/whatsap_ui_control_y/w.png'

# temp_image_path = 'C:/Users/szekiatpua/Downloads'
shutil.copyfile(source_image_path, temp_image_path)
#important to paste the copied image
# message_input.send_keys(Keys.CONTROL, 'v')

# Find the icon element by class name
# icon_element = driver.find_element_by_class_name("attach-menu-plus")
# Define the XPath for the element
icon_xpath = "//span[@data-icon='attach-menu-plus']"

# Wait for the element to be present on the page
icon_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, icon_xpath)))

# Now you can perform actions on the element
icon_element.click()


# Define the XPath for the file input element
file_input_xpath = "//input[@type='file' and @accept='image/*,video/mp4,video/3gpp,video/quicktime']"
# Wait for the file input element to be present on the page
file_input = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))

# Now you can perform actions on the file input element
# file_input.click()
file_input.send_keys("C:/Users/szekiatpua/Documents/GitHub/whatsap_ui_control_y/googlechromeversion.png")

# Define the XPath expression
xpath_expression = "//div[@title='Type a message']//div"

# Find all elements matching the XPath
elements = driver.find_elements(By.XPATH, xpath_expression)

# Iterate through the elements
for element in elements:
    try:
        # Check if the element is clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
    except:
        # If the element is not clickable, continue to the next element
        continue
    else:
        # If the element is clickable, perform actions on it
        element.click()
        # Send keys to the element
        element.send_keys("Your message here")
        # Break the loop since we found the clickable element
        break
        
# message_input.send_keys(Keys.ENTER) 

# Wait for the send button to be clickable
send_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Send']//span[@data-icon='send']"))
)

# Click the send button
send_button.click()


wait=WebDriverWait(driver,1000)
quit()

search_start_chat_button.send_keys(Keys.ENTER)  # Hit Enter

# Locate the message input textbox
message_input_xpath = '//div[@title="Type a message"]'
message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))

#IPPORATMT
#//button[@aria-label='Search or start new chat']/div[2]//span[@data-icon='search']
# Perform actions on the message input textbox
message_input.send_keys("Your message")  # Replace "Your message" with the text you want to send
message_input.send_keys(Keys.ENTER) 

# contact_path='//span[contains(@title,'+ target +')]'
# contact=wait.until(EC.presence_of_element_located((By.XPATH,contact_path)))
# contact.click()
# message_box_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
# message_box=wait.until(EC.presence_of_element_located((By.XPATH,message_box_path)))
# for x in range(number_of_times):
#     message_box.send_keys(message + Keys.ENTER)
#     time.sleep(0.2)
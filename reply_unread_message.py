from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re

options=webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/szekiatpua/AppData/Local/Google/Chrome/User Data")

driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win32\\chromedriver.exe', chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait=WebDriverWait(driver,100)
driver.maximize_window()

elements = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-icon='filter']")))
elements.click()

clickunread_xpath = "//span[contains(@data-icon, 'search-unread')]"
clickunread_xpath_clickrf = wait.until(EC.presence_of_element_located((By.XPATH, clickunread_xpath)))
clickunread_xpath_clickrf.click()

time.sleep(1)

message_input_xpath = "//span[contains(@aria-label, 'unread message')]"
message_input = wait.until(EC.presence_of_all_elements_located((By.XPATH, message_input_xpath)))

for hello in message_input: 
    aria_label = hello.get_attribute('aria-label')
    print(aria_label)
    numeric_value = int(re.search(r'\d+', aria_label).group())

    print("Numeric Value:", numeric_value)

    hello.click()

    message_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'message-in focusable-list-item')]")))

    last_three_elements = message_elements[-numeric_value:]

    for message_element in last_three_elements:
        message_content = message_element.text
        message_content_parts = message_content.split("\n")
        message_content_without_time = message_content_parts[0] 
        print(message_content_without_time)
        
    message_input_xpath = '//div[@title="Type a message"]'
    message_input = wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))

    time.sleep(1)

    message_input.send_keys("hello sis 2")
    
    send_button_xpath = "//span[@data-icon='send']"
    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
    send_button.click()





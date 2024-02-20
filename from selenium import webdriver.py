from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Documents\\ChromeDriver\\chromedriver_win32\\chromedriver.exe')
options=webdriver.ChromeOptions()

options.add_argument("user-data-dir=C:/Users/szekiatpua/AppData/Local/Google/Chrome/User Data")

driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win32\\chromedriver.exe', chrome_options=options)

#driver=webdriver.Chrome('C:\\Users\\szekiatpua\\Downloads\\chromedriver-win64 (2)\\chromedriver-win64\\chromedriver.exe',chrome_options=options)
driver.get("https://web.whatsapp.com/")
wait=WebDriverWait(driver,100)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time

options = webdriver.ChromeOptions()
service = Service("/API_EG/chromedriver")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

Username_EG="01014209"
PassWord_EG="Mi^mi^12345678901"

driver = webdriver.Chrome(service=service,options=options)

def LoginEG(_user,_password):
    #Going to login page
    driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
    current_url =driver.current_url

    #Enter Username and Password
    driver.find_element("id","inputUserName").send_keys(_user)
    driver.find_element("id","inputPassword").send_keys(_password)
    driver.find_element("id","submitBtn").click()
    #Waiting for another popup for click continue
    time.sleep(0.5)
    driver.find_element(By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]").click()
    time.sleep(1)

    if( current_url != driver.current_url):
        driver.close()
        return True
    else :
        driver.close()
        return False
    

if (LoginEG(Username_EG,PassWord_EG)) :
    print("PASS")
else :
    print("NOT PASS")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import pickle
import time
import os

start_time=time.time()
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

    if not (os.path.isfile("./cookies.pkl")):
        #Going to login page
        driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
        current_url = driver.current_url

        #Enter Username and Password
        driver.find_element("id","inputUserName").send_keys(_user)
        driver.find_element("id","inputPassword").send_keys(_password)
        driver.find_element("id","submitBtn").click()

        #Waiting for another popup for click continue
        time.sleep(0.5)
        driver.find_element(By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]").click()
        time.sleep(1)

        #Saving cookies file for login session.
        pickle.dump( driver.get_cookies() , open("./cookies.pkl","wb"))

    else :
        #Going to login page
        driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
        current_url = driver.current_url


    if( current_url != driver.current_url):
        return True
    else :
        driver.close()
        return False


if (LoginEG(Username_EG,PassWord_EG)) :
    print("PASS")
    f = open("./url_device.txt", "r",encoding="utf8")
    url_get=f.read().replace("\n","")
    url_get=url_get.replace("SNXXXXXXXXXX","HWTC0E22F3AB")
    driver.get(url_get)
    json_text = driver.find_element(By.XPATH,"//body/pre[@style='word-wrap: break-word; white-space: pre-wrap;']").text
    print(json_text)
else :
    print("NOT PASS")

end_time=time.time()
print(f"time usage : {round(end_time-start_time,2)}sec")
driver.close()
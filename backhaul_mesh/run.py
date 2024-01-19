from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import os
import pickle 
import time
import json
import pyautogui
logforwrite=""
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

Username_EG="01014209"
PassWord_EG="xxxxxxxxxx"



now = datetime.now()    
dt_string_ = now.strftime("%H")
now_time=int(dt_string_)

#while (11 <= now_time >12):
#    now = datetime.now()    
#    dt_string_ = now.strftime("%H")
#    now_time=int(dt_string_)
#    time.sleep(1)
#    print(dt_string_)
    


driver = webdriver.Chrome(ChromeDriverManager().install())




def LoginEG(_user,_password):
    #print(_user)
    #print(_password)
    #path = 'D:/addwan_huawei/' #กำหนด folder ที่จะให้ระบบทำงาน
    #os.chdir(path) #รัน Code เพื่อสั่งให้ระบบทำงานบน folder ที่ต้องการ    
    #Old URL driver.get('http://61.90.207.93:21180/web/res/web-framework/default.html#_cpehg-general-daily-management-menu')
    #New URL http://61.90.207.93:21180/web/iui/framework/login.html
    driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
    driver.find_element_by_id("details-button").click()
    driver.find_element_by_id("proceed-link").click()

    #driver.find_element_by_id("inputUserName").send_keys(_user)
    #driver.find_element_by_id ("inputPassword").send_keys(_password)
    #driver.find_element_by_id("submitBtn").click()
    driver.find_element("id","inputUserName").send_keys(_user)
    driver.find_element("id","inputPassword").send_keys(_password)
    driver.find_element("id","submitBtn").click()
    time.sleep(5)
    pyautogui.press('enter')  # press the Enter key    
    time.sleep(15)
    pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb"))
    #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    #Old URL driver.get('http://61.90.207.93:21180/web/res/web-framework/default.html#_cpehg-general-daily-management-menu')
    #New URL http://61.90.207.93:21180/web/iui/framework/default.html#_cpehg-general-daily-management-menu
    driver.get('https://10.50.27.136:21180/web/iui/framework/default.html#_cpehg-general-daily-management-menu')
    time.sleep(5)
    source = driver.page_source
    source =str(source)
    int_ChkLogIn=source.find("CPE Daily Management")
    if int_ChkLogIn > 1:
        print("Login pass\n")
        return('pass')
    else:
        print("Login fail")
        return("fail")  


    


if(LoginEG(Username_EG,PassWord_EG))=="pass":
    filename = "input.txt"
    filehandle = open(filename, 'r')
    int_x=0
    while True:
        # read a single line
        int_x=int_x+1
        print(int_x)
        line = filehandle.readline()
        if not line:
            break
        print(line)
        ss1=line
    
        ss1=str(ss1)
        ss1=ss1.replace("['","")
        ss1=ss1.replace("]'","")
        
        #//////////////////////////////////////////////////////////    
        f = open("./url_device_info4.txt", "r",encoding="utf8")
        url_get=f.read()
        f.close()
        url_get=url_get.replace("SNXXXXXXXXXX",str(ss1))       
        driver.get(url_get)    
        source2 = driver.page_source    
        input_f2=str(source2)
        #print(source2)    
        ss1.replace("\n","")  
        int_find_str=0
        int_find_str = source2.find("InternetGatewayDevice")
        adata=[]
        model=SW=wlan1status=wlan5status=wlan6status= bsssid1=bsssid5=bsssid6=ssid6=""       
        if int_find_str > 0:
            source2=source2.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
            source2=source2.replace('</pre></body></html>','')
            source2=source2.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
            source2=source2.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
            source2=source2.replace('</pre></body></html>','')
            #print(source2)     
            json_data = json.loads(source2)
            ONOFF="ONLINE"
                
            lentofjson=len(json_data['response']['data']['oidValues'])
            print("________________________________________________________________") 
            print(lentofjson)
            print("________________________________________________________________")   
            for x in range(19):                
                adata.append((json_data['response']['data']['oidValues'][x]['value'])) #WLANConfiguration.5.Status
               #adata.append((json_data['response']['data']['oidValues'][x]['value'])) #WLANConfiguration.5.Status
           
            
        else:
            print("OFFLINE")
            ONOFF="OFFLINE"
        
        #////////////////report///////////////////////
        ss1=ss1.replace('\n','')        
        
           
        now = datetime.now()    
        dt_string = now.strftime("%d/%m/%Y,%H:%M:%S")
        adata1=str(adata)
        adata1=adata1.replace("['","")
        adata1=adata1.replace("]'","")
        adata1=adata1.replace("'","")
        adata1=adata1.replace("]","")
        adata1=adata1.replace("[","")
            
        csvf=dt_string+","+ss1+","+ONOFF+","+adata1+"\n"
        print(csvf)
        
        f = open("P1.csv", "a",encoding="utf8")
        f.write(csvf)
        f.close()     
        
    
filehandle.close()
driver.close()
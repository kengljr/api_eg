from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
from datetime import timedelta
import pickle
import time
import json
from random import randint

start_time=time.time()
options = webdriver.ChromeOptions()
service = Service("/API_EG/chromedriver")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

current_time = datetime.strftime(datetime.now(),"%Y%m%d")
Username_EG="01014209"
PassWord_EG="Mi^mi^12345678901"

login_page = 'https://10.50.27.136:21180/web/iui/framework/login.html'

#driver = webdriver.Chrome(service=service,options=options)

#First define request_status = True before using Login function
request_status = True
def request_checking (request):
    response = Response()
    if not (request):
        response_msg = {"code":0,"msg":"Error","Value":"Request Body empty"}
        response.data=response_msg
        response.status_code=status.HTTP_400_BAD_REQUEST
        return response
    elif (request["Mesh_no"]==''):
        response_msg = {"code":0,"msg":"Error","Value":"Missing MeshNumber"}
        response.data=response_msg
        response.status_code=status.HTTP_400_BAD_REQUEST
        return response
    elif (request["DSN"]==''):
        response_msg = {"code":0,"msg":"Error","Value":"Missing DSN"}
        response.data=response_msg
        response.status_code=status.HTTP_400_BAD_REQUEST
        return response
    elif (int(request["Mesh_no"])>4 or int(request["Mesh_no"])<1) :
        response_msg = {"code":0,"msg":"Error","Value":"MeshNumber not in range"}
        response.data=response_msg
        response.status_code=status.HTTP_400_BAD_REQUEST
        return response
    else:
        response.data=request
        response.status_code=status.HTTP_200_OK
        return response

def create_cookie_session (_user,_password):
    driver = webdriver.Chrome(service=service,options=options)
    with open('result_test.txt', 'a') as the_file:
        the_file.write(f"PID:{driver.service.process.pid} executed (create cookie session function)\n")

    driver.get(login_page)
    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 30)

    #Enter Username and Password
    wait.until(EC.visibility_of_element_located((By.ID, 'inputUserName'))).send_keys(_user)
    wait.until(EC.visibility_of_element_located((By.ID, 'inputPassword'))).send_keys(_password)
    driver.find_element("id","submitBtn").click()

    wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]"))).click()
    #driver.find_element(By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]").click()
    time.sleep(1)

    #Saving cookies file for login session.
    pickle.dump( driver.get_cookies() , open("/API_EG/backhaul_mesh/cookies.pkl","wb"))
    return driver

def load_driver():
    driver = webdriver.Chrome(service=service,options=options)
    with open('result_test.txt', 'a') as the_file:
        the_file.write(f"PID:{driver.service.process.pid} executed (load_driver function)\n")
    driver.get(login_page)
    cookies = pickle.load(open("/API_EG/backhaul_mesh/cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)
    return driver,login_page != driver.current_url
    
def connect_eg() :
    global request_status
    driver = create_cookie_session(Username_EG ,PassWord_EG)
    time.sleep(2)
    request_status = True
    with open('result_test.txt', 'a') as the_file:
        the_file.write(f"PID:{driver.service.process.pid} finished\n")
    driver.close()
    driver.quit()


def random_delay():
    a = randint(0,100)/100
    time.sleep(a)
    print(a)

def queue_load_driver():
    global request_status
    random_delay()
    
    #First process which be executed will be in this if statement
    if (request_status):

        #Set request_status to False to make others process end this If statement.
        request_status = False
        with open('result_test.txt', 'a') as the_file:
            the_file.write(f'{time.time()}: Debug No Cookies\n')
        connect_eg()
        print("checking")
    
    while not (request_status):
        time.sleep(0.5)
    return load_driver()

def LoginEG(_user,_password):
    global request_status
    if not (os.path.isfile("/API_EG/backhaul_mesh/cookies.pkl")):
        driver,status = queue_load_driver()
    else:
        driver,status = load_driver()
    #Login Successful
    if(status):
        return driver,status
    
    with open('result_test.txt', 'a') as the_file:
        the_file.write(f'{time.time()} : Debug timeout Cookies\n')
    return queue_load_driver()

def device_check(backhaul_type,mesh_no,serial_number):
    global request_status
    driver,checking = LoginEG(Username_EG,PassWord_EG)
    if (checking) :
        # request_status = True
        print("PASS")
        f = open("/API_EG/backhaul_mesh/url_device.txt", "r",encoding="utf8")
        url_get=f.read().replace("\n","")
        url_get=url_get.replace("SNXXXXXXXXXX",serial_number)
        driver.get(url_get)
        json_text = json.loads(driver.find_element(By.XPATH,"//body/pre[@style='word-wrap: break-word; white-space: pre-wrap;']").text)
        driver.close()
        #driver.quit()
        try :
            for member in json_text["response"]["data"]["oidValues"]:
                if  (backhaul_type in member["oid"]) and (f"Agent.{mesh_no}" in member["oid"]):
                    return member["value"]
            return json_text["response"]["data"]["oidValues"]
        except KeyError :
            open("/API_EG/backhaul_mesh/debug_log.txt","a+").write(str(json_text)+"\n")
            return None
    else :
        driver.close()
        driver.quit()
        request_status = False
        print("NOT PASS")
        return False
    
    driver.close()
    end_time=time.time()
    #print(f"time usage : {round(end_time-start_time,2)}sec")

@api_view(('GET',))
def snippet_detail(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        return Response({"testt":"Testing"})

@api_view(('GET','POST','PUT',))
def get_mediatype_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """
    client_ip = request.META.get('REMOTE_ADDR')
    ip_list = open("/API_EG/backhaul_mesh/allow_ip.txt","r").read().split("\n")
    if(client_ip in ip_list) :
  
        if request.method == 'GET' :
            #print(request.data)
            log("request",request.method,request,request.data)
            #print(request.data)
        
            #Checking request.data return back response_msg and http_code
            request_result = request_checking(request.data)

            #Checking that input json data is correct form. 
            if (request_result.status_code == status.HTTP_200_OK) :
                result = device_check("MediaType",request.data["Mesh_no"],request.data["DSN"])
                response_msg = {"code":0,"msg":"GETMediaTypebackhaulmesh(x)","Value":result}
                status_code = request_result.status_code
                if(result is None ) :
                    response_msg = {"code":0,"msg":"Error","Value":"DSN Not Found"}
                    status_code=status.HTTP_400_BAD_REQUEST
                elif not(result) :
                    response_msg = {"code":0,"msg":"Error","Value":"Cannot login to EG Please try again in a few minutes."}
                    status_code=status.HTTP_400_BAD_REQUEST
            else :
                response_msg= request_result.data
                status_code = request_result.status_code
            log("response",request.method,request,response_msg)
            
        else :
            log("request",request.method,request,request.data)
            response_msg = {"code":0,"msg":"Error","Value":"Method not allow"}
            status_code=status.HTTP_400_BAD_REQUEST
            log("response",request.method,request,response_msg)
    else :
        response_msg = {"code":0,"msg":"Error","Value":"You are not allow to access this."}
        log("request",request.method,request,request.data)
        log("response",request.method,request,response_msg)
        status_code=status.HTTP_400_BAD_REQUEST
    return Response(response_msg,status_code)

#We need to use @api_view for each function.
@api_view(('GET','PUT','POST',))
def get_signal_strength_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """
    client_ip = request.META.get('REMOTE_ADDR')
    ip_list = open("/API_EG/backhaul_mesh/allow_ip.txt","r").read().split("\n")
    if(client_ip in ip_list) :

        if request.method == 'GET' :

            log("request",request.method,request,request.data)
            #Checking request.data return back response_msg and http_code
            request_result = request_checking(request.data)

            if (request_result.status_code == status.HTTP_200_OK) :   
                result = device_check("SignalStrength",request.data["Mesh_no"],request.data["DSN"])
                response_msg = {"code":0,"msg":"SignalStrengthbackhaulmesh(x)","Value":result}
                status_code = request_result.status_code
                if(result is None ) :
                    response_msg = {"code":0,"msg":"Error","Value":"DSN Not Found"}
                    status_code=status.HTTP_400_BAD_REQUEST
                elif not(result) :
                    response_msg = {"code":0,"msg":"Error","Value":"Cannot login to EG Please try again in a few minutes."}
                    status_code=status.HTTP_400_BAD_REQUEST
            else :
                response_msg= request_result.data
                status_code = request_result.status_code
            log("response",request.method,request,response_msg)
            
        else :
            log("request",request.method,request,request.data)
            response_msg = {"code":0,"msg":"Error","Value":"Method not allow"}
            status_code=status.HTTP_400_BAD_REQUEST
            log("response",request.method,request,response_msg)
    else :
        response_msg = {"code":0,"msg":"Error","Value":"You are not allow to access this."}
        status_code=status.HTTP_400_BAD_REQUEST
    return Response(response_msg,status_code)

@api_view(('GET','PUT','POST',))
def get_phy_rate_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """
    client_ip = request.META.get('REMOTE_ADDR')
    ip_list = open("/API_EG/backhaul_mesh/allow_ip.txt","r").read().split("\n")
    if(client_ip in ip_list) :

        if request.method == 'GET' :

            log("request",request.method,request,request.data)
            #Called function
            request_result = request_checking(request.data)

            if (request_result.status_code == status.HTTP_200_OK) :   
                result = device_check("PHYRate",request.data["Mesh_no"],request.data["DSN"])
                response_msg = {"code":0,"msg":"GETPHYRatebackhaulmesh(x)","Value":result}
                status_code = request_result.status_code
                if(result is None ) :
                    response_msg = {"code":0,"msg":"Error","Value":"DSN Not Found"}
                    status_code=status.HTTP_400_BAD_REQUEST
                elif not(result) :
                    response_msg = {"code":0,"msg":"Error","Value":"Cannot login to EG Please try again in a few minutes."}
                    status_code=status.HTTP_400_BAD_REQUEST
            else :
                response_msg= request_result.data
                status_code = request_result.status_code
            log("response",request.method,request,response_msg)
            
        else :
            log("request",request.method,request,request.data)
            response_msg = {"code":0,"msg":"Error","Value":"Method not allow"}
            status_code=status.HTTP_400_BAD_REQUEST
            log("response",request.method,request,response_msg)
    else :
        response_msg = {"code":0,"msg":"Error","Value":"You are not allow to access this."}
        status_code=status.HTTP_400_BAD_REQUEST
        log("request",request.method,request,request.data)
        log("response",request.method,request,response_msg)
    return Response(response_msg,status_code)

@api_view(('GET','PUT','POST',))
def get_serial_number_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """
    client_ip = request.META.get('REMOTE_ADDR')
    ip_list = open("/API_EG/backhaul_mesh/allow_ip.txt","r").read().split("\n")
    if(client_ip in ip_list) :
        if request.method == 'GET' :
            log("request",request.method,request,request.data)
            #Called function
            request_result = request_checking(request.data)

            if (request_result.status_code == status.HTTP_200_OK) :   
                result = device_check("SerialNumber",request.data["Mesh_no"],request.data["DSN"])
                response_msg = {"code":0,"msg":"GETSerialNumberbackhaulmesh(x)","Value":result}
                status_code = request_result.status_code
                if(result is None ) :
                    response_msg = {"code":0,"msg":"Error","Value":"DSN Not Found"}
                    status_code=status.HTTP_400_BAD_REQUEST

                elif not(result) :
                    response_msg = {"code":0,"msg":"Error","Value":"Cannot login to EG Please try again in a few minutes."}
                    status_code=status.HTTP_400_BAD_REQUEST
            else :
                response_msg= request_result.data
                status_code = request_result.status_code
            log("response",request.method,request,response_msg)
            
        else :
            log("request",request.method,request,request.data)
            response_msg = {"code":0,"msg":"Error","Value":"Method not allow"}
            status_code=status.HTTP_400_BAD_REQUEST
            log("response",request.method,request,response_msg)
    else :
        response_msg = {"code":0,"msg":"Error","Value":"You are not allow to access this."}
        status_code=status.HTTP_400_BAD_REQUEST
        log("request",request.method,request,request.data)
        log("response",request.method,request,response_msg)
    return Response(response_msg,status_code)

@api_view(('GET',))
def get_log(request,time):
    
    client_ip = request.META.get('REMOTE_ADDR')
    ip_list = open("/API_EG/backhaul_mesh/allow_ip.txt","r").read().split("\n")
    if not (client_ip in ip_list) :
        response_msg = {"code":0,"msg":"Error","Value":"You are not allow to access this."}
        status_code=status.HTTP_400_BAD_REQUEST
        log("request",request.method,request,request.data)
        log("response",request.method,request,response_msg)
        return Response(response_msg,status_code)
    path=f"log/backhaul_mesh_api_{time}.log"
    response_msg= open(path, "r").read().split('\n')[-100:]
    return Response(response_msg,status=status.HTTP_200_OK)


def log(action,request_method,request,body_detail):
    current_time = datetime.strftime(datetime.now(),"%Y%m%d")
    path=f"log/backhaul_mesh_api_{current_time}.log"
    client_ip = request.META.get('REMOTE_ADDR')
    url = request.path_info # from where url
    #body_detail = request.data #What they send or what we send
    timestamp = datetime.strftime(datetime.now(),"%Y/%m/%d %H:%M:%S")


    log_string = f"{timestamp}|{action}|{request_method}|{client_ip}|{url}|{body_detail}\n"
    #print(log_string)
    if (os.path.isfile(path)):
        file = open(path,'a')
    else :
        file = open(path,'w')
        file.write("timestamp|action|request_method|client_ip|path|body_detail\n")
    file.write(log_string)
    file.close()

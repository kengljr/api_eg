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

driver = webdriver.Chrome(service=service,options=options)
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
    global driver
    driver = webdriver.Chrome(service=service,options=options)
    driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 30)

    #Enter Username and Password
    wait.until(EC.visibility_of_element_located((By.ID, 'inputUserName'))).send_keys(_user)
    #driver.find_element("id","inputUserName").send_keys(_user)
    #driver.find_element("id","inputPassword").send_keys(_password)
    wait.until(EC.visibility_of_element_located((By.ID, 'inputPassword'))).send_keys(_password)
    driver.find_element("id","submitBtn").click()

    #Waiting for another popup for click continue
    #time.sleep(0.5)
    wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]"))).click()
    #driver.find_element(By.XPATH,"//div[@class='bootbox modal fade bootbox-confirm in']/div/div/div[3]/button[2]").click()
    time.sleep(1)

    #Saving cookies file for login session.
    pickle.dump( driver.get_cookies() , open("/API_EG/backhaul_mesh/cookies.pkl","wb"))
    
def LoginEG(_user,_password):
    global driver
    global request_status
    #Going to login page
    driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
    current_url = driver.current_url

    if not (os.path.isfile("/API_EG/backhaul_mesh/cookies.pkl")):
        create_cookie_session(Username_EG,PassWord_EG)

    # else :
    #     threshold = timedelta(minutes=2) # can also be minutes, seconds, etc.
    #     filetime = os.path.getmtime("/API_EG/backhaul_mesh/cookies.pkl") # filename is the path to the local file you are refreshing
    #     now = time.time()
    #     delta_time = timedelta(seconds=now-filetime)

    #     #Checking if cookies session is more than 5 minutes so we need to remove this and create new session again.
    #     if(delta_time > threshold) :
    #         os.remove("/API_EG/backhaul_mesh/cookies.pkl")
    #         driver.close()
    #         #Close session before open new session.
    #         create_cookie_session(Username_EG,PassWord_EG)
        

    #Load cookies to login into website by previous session.       
    cookies = pickle.load(open("/API_EG/backhaul_mesh/cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(1.5)

    if( current_url != driver.current_url):
        return True
    else :
        if(request_status) :
            request_status = False
            create_cookie_session(Username_EG,PassWord_EG)
            request_status = True

        else :
            while not (request_status):
                time.sleep(0.5)
        return current_url != driver.current_url

def device_check(backhaul_type,mesh_no,serial_number):
    global request_status
    global driver
    checking = LoginEG(Username_EG,PassWord_EG)
    if (checking) :
        request_status = True
        print("PASS")
        f = open("/API_EG/backhaul_mesh/url_device.txt", "r",encoding="utf8")
        url_get=f.read().replace("\n","")
        url_get=url_get.replace("SNXXXXXXXXXX",serial_number)
        driver.get(url_get)
        json_text = json.loads(driver.find_element(By.XPATH,"//body/pre[@style='word-wrap: break-word; white-space: pre-wrap;']").text)
        #print(json_text)
        try :
            for member in json_text["response"]["data"]["oidValues"]:
                if  (backhaul_type in member["oid"]) and (f"Agent.{mesh_no}" in member["oid"]):
                    return member["value"]
            return json_text["response"]["data"]["oidValues"]
        except KeyError :
            return None
    else :
        request_status = False
        print("NOT PASS")
        return False
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

    if request.method == 'GET' :
        #print(request.data)
        log("request",request.method,request,request.data)
        #print(request.data)
       
        #Checking request.data return back response_msg and http_code
        request_result = request_checking(request.data)

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

    return Response(response_msg,status_code)

#We need to use @api_view for each function.
@api_view(('GET','PUT','POST',))
def get_signal_strength_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

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

    return Response(response_msg,status_code)

@api_view(('GET','PUT','POST',))
def get_phy_rate_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

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

    return Response(response_msg,status_code)

@api_view(('GET','PUT','POST',))
def get_serial_number_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

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

    return Response(response_msg,status_code)

@api_view(('GET',))
def get_log(request,time):
    path=f"log/backhaul_mesh_api_{time}.log"
    response_msg= open(path, "r")
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
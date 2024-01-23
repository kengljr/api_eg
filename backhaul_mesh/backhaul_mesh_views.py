from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
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
path=f"log/backhaul_mesh_api_{current_time}.log"

Username_EG="01014209"
PassWord_EG="Mi^mi^12345678901"

driver = webdriver.Chrome(service=service,options=options)

def LoginEG(_user,_password):
    #Going to login page
    driver.get('https://10.50.27.136:21180/web/iui/framework/login.html')
    if not (os.path.isfile("/API_EG/backhaul_mesh/cookies.pkl")):
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
        pickle.dump( driver.get_cookies() , open("/API_EG/backhaul_mesh/cookies.pkl","wb"))

    else :
        current_url = driver.current_url
        cookies = pickle.load(open("/API_EG/backhaul_mesh/cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(2)

    if( current_url != driver.current_url):
       # driver.close()
        return True
    else :
       # driver.close()
        return False

def device_check(backhaul_type,mesh_no,serial_number):
    checking = LoginEG(Username_EG,PassWord_EG)
    if (checking) :
        print("PASS")
        f = open("./url_device.txt", "r",encoding="utf8")
        url_get=f.read().replace("\n","")
        url_get=url_get.replace("SNXXXXXXXXXX",serial_number)
        driver.get(url_get)
        json_text = json.loads(driver.find_element(By.XPATH,"//body/pre[@style='word-wrap: break-word; white-space: pre-wrap;']").text)
       # print(json_text)
        for member in json_text["response"]["data"]["oidValues"]:
            if  (backhaul_type in member["oid"]) and (f"Agent.{mesh_no}" in member["oid"]):
                return member["value"]
        return json_text["response"]["data"]["oidValues"]
    else :
        print("NOT PASS")
    end_time=time.time()
    print(f"time usage : {round(end_time-start_time,2)}sec")

@api_view(('GET',))
def snippet_detail(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET':
        return Response({"testt":"Testing"})

@api_view(('GET',))
def get_mediatype_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET' :
        #print(request.data)
        log("request",request,request.data)
        print(request.data)
        #Called function
        if not (request.data):
            response_msg = {"code":0,"msg":"Error","Value":"Request Body empty"}
        elif (request.data["Mesh_no"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing MeshNumber"}
        elif (request.data["DSN"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing DSN"}
        elif (int(request.data["Mesh_no"])>4) :
            response_msg = {"code":0,"msg":"Error","Value":"MeshNumber not in range"}

        else:
            result = device_check("MediaType",request.data["Mesh_no"],request.data["DSN"])
            response_msg = {"code":0,"msg":"GETMediaTypebackhaulmesh","Value":result}
        log("response",request,response_msg)
        return Response(response_msg)

    elif request.method == 'PUT':
        log("request",request,request.data)
        response_msg = {"code":0,"msg":"Error","Value":"Methrod not allow"}
        log("response",request,response_msg)
        return Response(response_msg)

    elif request.method == 'POST':
        log("request",request,request.data)
        response_msg = {"code":0,"msg":"Error","Value":"Methrod not allow"}
        log("response",request,response_msg)
        return Response(response_msg)



#We need to use @api_view for each function.
@api_view(('GET',))
def get_signal_strength_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET' :

        log("request",request,request.data)
        #Called function
        if not (request.data):
            response_msg = {"code":0,"msg":"Error","Value":"Request Body empty"}
        elif (request.data["Mesh_no"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing MeshNumber"}
        elif (request.data["DSN"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing DSN"}
        elif (int(request.data["Mesh_no"])>4) :
            response_msg = {"code":0,"msg":"Error","Value":"MeshNumber not in range"}
        else :
            result = device_check("SignalStrength",request.data["Mesh_no"],request.data["DSN"])
            response_msg = {"code":0,"msg":"GETSignalStrengthbackhaulmesh(x)","Value":result}
        log("response",request,response_msg)
        return Response(response_msg)

@api_view(('GET',))
def get_phy_rate_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET' :

        log("request",request,request.data)
        #Called function
        if not (request.data):
            response_msg = {"code":0,"msg":"Error","Value":"Request Body empty"}
        elif (request.data["Mesh_no"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing MeshNumber"}
        elif (request.data["DSN"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing DSN"}
        elif (int(request.data["Mesh_no"])>4) :
            response_msg = {"code":0,"msg":"Error","Value":"MeshNumber not in range"}
        else :
            result = device_check("PHYRate",request.data["Mesh_no"],request.data["DSN"])
            response_msg = {"code":0,"msg":"GETPHYRatebackhaulmesh(x)","Value":result}
        log("response",request,response_msg)
        return Response(response_msg)

@api_view(('GET',))
def get_serial_number_backhaul_mesh(request):
    """
    Retrieve, update or delete a code snippet.
    """

    if request.method == 'GET' :
        log("request",request,request.data)
        #Called function
        if not (request.data):
            response_msg = {"code":0,"msg":"Error","Value":"Request Body empty"}
        elif (request.data["Mesh_no"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing MeshNumber"}
        elif (request.data["DSN"]==''):
            response_msg = {"code":0,"msg":"Error","Value":"Missing DSN"}
        elif (int(request.data["Mesh_no"])>4) :
            response_msg = {"code":0,"msg":"Error","Value":"MeshNumber not in range"}
        else :
             result = device_check("SerialNumber",request.data["Mesh_no"],request.data["DSN"])
             response_msg = {"code":0,"msg":"GETSerialNumberbackhaulmesh(x)","Value":result}
        log("response",request,response_msg)
        return Response(response_msg)

@api_view(('GET',))
def get_log(request):
    response_msg= open(path, "r")
    return Response(response_msg)


def log(action,request,body_detail):
    client_ip = request.META.get('REMOTE_ADDR')
    url = request.path_info # from where url
    #body_detail = request.data #What they send or what we send
    timestamp = datetime.strftime(datetime.now(),"%Y/%m/%d %H:%M:%S")
    log_string = f"{timestamp}|{action}|{client_ip}|{url}|{body_detail}\n"
    print(log_string)
    if (os.path.isfile(path)):
        file = open(path,'a')
    else :
        file = open(path,'w')
        file.write("timestamp|action|client_ip|path|body_detail\n")
    file.write(log_string)
    file.close()
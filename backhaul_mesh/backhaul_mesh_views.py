from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
import os
from datetime import datetime


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
        #Called function
        response_msg = {"code":0,"msg":"GETMediaTypebackhaulmesh","Value":request.data}
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
        response_msg = {"code":0,"msg":"GETSignalStrengthbackhaulmesh(x)","Value":request.data}
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
        response_msg = {"code":0,"msg":"GETPHYRatebackhaulmesh(x)","Value":request.data}
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
        response_msg = {"code":0,"msg":"GETSerialNumberbackhaulmesh(x)","Value":request.data}
        log("response",request,response_msg)
        return Response(response_msg)
    

def log(action,request,body_detail):
    current_time = datetime.strftime(datetime.now(),"%Y%m%d")
    path=f"/app/api_eg/log/backhaul_mesh_api_{current_time}.log"
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
    
    


#backhaul_mesh_api_20231203.log

    

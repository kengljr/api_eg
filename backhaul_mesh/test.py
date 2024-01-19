import requests
import json

r = requests.get('http://localhost:8000/backhaul_mesh/GETSerialNumberbackhaulmesh', json={
    "Mesh_no":1,
    "DSN":"SCOMXXXXX"
})

print(r.json())
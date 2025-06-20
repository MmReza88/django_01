from mfrc522 import SimpleMFRC522
import requests
import time

server_ip = "192.168.30.224"
server_port = 8000
totem_id = "controler_123"
secret_token = "aevJFz4xFHNUK0gCohc1"

while True:
    reader = SimpleMFRC522()
    id, _ = reader.read()

    print(f"http://{server_ip}:{server_port}/ctrl/badge/{totem_id}{id}/")
    response = requests.get(f"http://{server_ip}:{server_port}/ctrl/badge/{totem_id}{id}/")
    print(response.text)
    
    time.sleep(5)

import requests
import json
import hashlib


def createfiles(path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    
    with open(path, "rb") as file:
        file_data = file.read()

    sha256_hash = hashlib.sha256(file_data).hexdigest()

    
    payload = {
        "file": file_data
    }

    # poprawic w env dodac
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJmODMyNmM0MC1iZDMxLTRjNDYtOGJmYy0xOGYzNTQzYzg4MGYiLCJlbWFpbCI6IjB4MmY0MzBjMWU3N2I5MTAxOWM3NmJkMjNkNmY2ZmZhOWY4MmFiMGE3MkBldGhlcm1haWwuaW8iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX0seyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiYzk4MDRjMWMxZTUzN2ViYzQwMjgiLCJzY29wZWRLZXlTZWNyZXQiOiIxYzg0OGEzYWIyNDAxZDFhNWVhNjQyODcyMTVlZTRiNmMzNzFhMmQyYzhkNjcyNTk2OTI4MGE0MjY4M2I4YWQxIiwiaWF0IjoxNzE1MTA4ODY0fQ.QdWVuKQL-SOsEO8qL6oIB0XG3KnHhNNqnvcrfK_g1u0"
    }

    # Wyślij żądanie POST do Pinaty, aby przypiąć plik
    response = requests.post(url, files=payload, headers=headers)

    response_json = json.loads(response.text)


    ipfsHash=response_json['IpfsHash']
    return ipfsHash,sha256_hash



ipfsHash,sha =createfiles("/home/kali/Desktop/new_git/BlockchainLogger/snake_game/test3.txt"
)
print (sha)

   

'''
print("list pined files")

url = "https://api.pinata.cloud/data/pinList"

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJmODMyNmM0MC1iZDMxLTRjNDYtOGJmYy0xOGYzNTQzYzg4MGYiLCJlbWFpbCI6IjB4MmY0MzBjMWU3N2I5MTAxOWM3NmJkMjNkNmY2ZmZhOWY4MmFiMGE3MkBldGhlcm1haWwuaW8iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX0seyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiYzk4MDRjMWMxZTUzN2ViYzQwMjgiLCJzY29wZWRLZXlTZWNyZXQiOiIxYzg0OGEzYWIyNDAxZDFhNWVhNjQyODcyMTVlZTRiNmMzNzFhMmQyYzhkNjcyNTk2OTI4MGE0MjY4M2I4YWQxIiwiaWF0IjoxNzE1MTA4ODY0fQ.QdWVuKQL-SOsEO8qL6oIB0XG3KnHhNNqnvcrfK_g1u0"}

response = requests.request("GET", url, headers=headers)

print(response.text)
'''


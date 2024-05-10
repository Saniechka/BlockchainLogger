import click
import json
from web3 import Web3
from hexbytes import HexBytes
import time
import requests
import hashlib
import os
from aes import aesDecrypt,aesEncrypt,getAESKey
from rsa import rsaEncrypt, get_private_key, get_public_key, rsaDecrypt,  generate_all_keys



def load_config():
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        print("config file problem")
        return None


def my_wallet_address():
    config_data = load_config()
    if config_data is None:
        return None

    wallet_address = config_data.get('wallet_address')
    return wallet_address

#help function
def get_contract_and_credentials():
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    config_data = load_config()
    if config_data is None:
        return None, None, None, None

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url)) 
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
     

    return contract, wallet_address, private_key,chain_id,web3

def execute_transaction(contract, function_name, args, chain_id, wallet_address, private_key, web3):
    # Budowanie transakcji w zależności od funkcji
    transaction = getattr(contract.functions, function_name)(*args).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    # Podpisanie transakcji
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Wysłanie transakcji
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Poczekanie na potwierdzenie transakcji
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt



def view_my_logs_sk(output_file, encrypted, company):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
    
   
    my_logs = contract.functions.getMyLogs(encrypted, company).call({'from': wallet_address})

    if encrypted :
        return my_logs
    
    if output_file:
        # Zapisz logi do pliku, jeśli podano parametr --file
        with open(output_file, 'w') as f:
            f.write("My Logs:\n")
            for my_log in my_logs:
                log = my_log[0]
                f.write(str(log) + '\n')
        print(f"Your logs saved to {output_file}")
    else:
        # Wyświetl logi w terminalu
        print("My Logs:")
        for my_log in my_logs:
            print(my_log)



def view_user_logs_sk(address,output_file, encrypted, company):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
    
   
    my_logs = contract.functions.getUserLogs(address,encrypted, company).call({'from': wallet_address})

    if encrypted :
        return my_logs
    
    if output_file:
        # Zapisz logi do pliku, jeśli podano parametr --file
        with open(output_file, 'w') as f:
            f.write("User Logs:\n")
            for my_log in my_logs:
                f.write(str(my_log) + '\n')
        print(f"Your logs saved to {output_file}")
    else:
        # Wyświetl logi w terminalu
        print("My Logs:")
        for my_log in my_logs:
            print(my_log)



def createHashes(path):


    file_path = "variable.json"

    with open(file_path, "r") as file:
        data1 = json.load(file)

    url = data1[ipfs_url]
    authorization_token= data1["ipfs_jwt"]

    
    with open(path, "rb") as file:
        file_data = file.read()

    sha256_hash = hashlib.sha256(file_data).hexdigest()

    
    payload = {
        "file": file_data
    }

    # poprawic w env dodac
    headers = {
        "Authorization": authorization_token
    }

    # Wyślij żądanie POST do Pinaty, aby przypiąć plik
    response = requests.post(url, files=payload, headers=headers)

    response_json = json.loads(response.text)


    ipfsHash=response_json['IpfsHash']
    return ipfsHash,sha256_hash


def save_logs_to_file(logs, file_path):
    with open(file_path, 'a') as file:
        for log in logs:
            file.write(log + '\n')
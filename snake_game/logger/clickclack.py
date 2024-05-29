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
from help import  load_config,my_wallet_address,get_contract_and_credentials,execute_transaction,view_my_logs_sk,view_user_logs_sk,createHashes,save_logs_to_file


@click.group()
@click.pass_context
def cli(ctx):
    pass

###############################
# login auth  func

# init change?
# dopisac tworzenie  key
@cli.command(help='Initialization')
@click.option('--wallet_address', help='Your wallet address ')
@click.option('--private_key', help='Your private key.')

def init(wallet_address, private_key): 

    file_path = "variable.json"

    with open(file_path, "r") as file:
        data1 = json.load(file)

    generate_all_keys(wallet_address)
    if not wallet_address or not private_key:
        print("Error: Please provide both wallet address and private key.")
        return
    

    sepolia_rpc_url = data1["sepolia_rpc_url"]
    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    print(f"Is connected: {web3.is_connected()}")  # Is connected: True
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)

    chain_id = web3.eth.chain_id
    contract_address = data1["contract_address"] #wpisac jako zmienna
    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi) 
    print(contract)
    config_data = {
        'wallet_address': wallet_address,
        'private_key': private_key,
        'chain_id': chain_id,
        'contract_address': contract_address,
        'sepolia_rpc_url' : sepolia_rpc_url
       
    }
    with open('config.json', 'w') as file:
        json.dump(config_data, file)




@cli.command(help = 'comand for logging')
@click.option('--login', help='User login')
@click.option('--password', help='User password')
def login(login, password):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     

    receipt = execute_transaction(
        contract, 'login', [login, password], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print("login success")



@cli.command(help ='log out')
def logout( ):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    receipt = execute_transaction(contract, 'logoutUser', [], chain_id, wallet_address, private_key, web3)
    print(receipt)

    if receipt.status == 1:
        print("logout succes")



@cli.command(help= 'adminOnly register new user')
@click.option('--address', help='New user address')
@click.option('--login', help='New user login')
@click.option('--password', help='New user password')

def register_user(address, login, password):

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     
    transaction_data = {
        'address': address,
        'login': login,
        'password': password
    }

# Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'registerUser', [address, login, password], chain_id, wallet_address, private_key, web3   
    )

    print(receipt)
    if receipt.status == 1:
        print('User registered success')




@cli.command(help = 'ADMINONLY get user profile')
@click.option('--address', help='User address')
def getUserDetails( address):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    
    result1 = contract.functions.getUserDetails(address).call({'from': wallet_address})
    


    result = result1.split(",")
    
    name = result[0]
    password = result[1]
    is_logged_in = result[2]
    role = result[3]


    print("Name:", name)
    print("Password:", password)
    print("Is Logged In:", is_logged_in)
    print("Role:", role)
   
    

@cli.command(help = 'adminOnly add new admin')
@click.option('--address', help='New admin address')

def set_Admin(address):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'setAdmin', [address], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('OK')
     


@cli.command(help= 'adminOnly setSuperUser')
@click.option('--address', help='User address')

def set_SuperUser(address):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'setSuperuser', [address], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('OK')



@cli.command(help= 'adminOnly change another user password')
@click.option('--address', help='User address')
@click.option('--new_password', help='New password')

def change_user_password( address, new_password):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'changeUserPassword', [address, new_password], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('Password changed')




@cli.command(help='adminOnly change another user name')
@click.option('--address', help='User address')
@click.option('--new_name', help='New user name')
def change_user_name(address, new_name):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

   
    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'changeUserName', [address, new_name], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('Name changed')



@cli.command(help = 'change password')
@click.option('--new_password', help='New password')

def change_my_password(new_password):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'changeMyPassword', [new_password], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('Password changing success')
     


@cli.command(help= 'onlyAdmin get list of all users')
def get_all_users():

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     
    users = contract.functions.getAllUsers().call({'from': wallet_address})

    print("List of all users:")
    for user_address in users:
        print(user_address)



@cli.command(help= 'See my status')
def view_my_role( ):
    
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     
    user_status = contract.functions.viewMyRole().call({'from': wallet_address})
    
    print(user_status)



@cli.command(help = 'see admin addres')
def adminAddres():
    
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    admin_address = contract.functions.adminAddress().call({'from': wallet_address})

    print("AdminAddres:", admin_address)



@cli.command(help = 'see superuser addres')
def superuserAddres():

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     
    superuser_address = contract.functions.superuserAddress().call({'from': wallet_address})

    print("superuserAddres:", admin_address)



@cli.command(help= 'adminOnly check user role')
@click.option('--address', help='User address')
def check_User_Role(address):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    address = Web3.to_checksum_address(address)
    user_status = contract.functions.checkUserRole(address).call({'from': wallet_address})

    print("User status:", user_status)

@cli.command(help= 'check if user logged')
@click.option('--address', help='User address')
def is_User_Logged_In( address):

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    is_logged_in = contract.functions.isUserLoggedIn(address).call({'from': wallet_address})
    
    print("Is user logged in:", is_logged_in)

####################################################
#################################################
#add file data

@cli.command(help='add file data')
@click.option('--filename', help='FILENAME')
@click.option('--path', help='PATH')
def add_file_data(filename, path):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
    
    # Check if filename and path are provided
    if not filename or not path:
        print("Error: Please provide both filename and path.")
        return
    
    # Create hashes
    ipfsHash, fileHash = createHashes(path)
    
    # Check if createHashes function returns valid hashes
    if not ipfsHash or not fileHash:
        print("Error: Failed to create hashes.")
        return

    # Get current time
    dateAdded = int(time.time())

    # Extract file extension for fileType
    fileType = path.split('.')[-1]
    print(fileHash)
    

    try:
        # Execute transaction
        receipt = execute_transaction(
            contract, 'add', [ipfsHash, fileHash, filename, fileType, dateAdded], chain_id, wallet_address, private_key, web3
        )
        
        # Check if transaction was successful
        if receipt.status == 1:
            print('FILE ADDED SUCCESS')
        else:
            print('Error: File addition failed.')
    except Exception as e:
        print('Error:', e)



@cli.command(help='get file data by file hash')
@click.option('--file_hash', help='File hash')
def get_filed_data(file_hash):
    if not file_hash:
        print("Error: Please provide the file hash.")
        return

    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
     
    file_data = contract.functions.get(file_hash).call({'from': wallet_address})

    
    print("File Hash:", file_data[0])
    print("IPFS Hash:", file_data[1])
    print("File Name:", file_data[2])
    print("File Type:", file_data[3])
    print("Date Added:", file_data[4])
    print("Exist:", file_data[5])

#############################################################################
#viewMyLogs

@cli.command(help= 'view my logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_my_logs(output_file):
    view_my_logs_sk(output_file,False,False)

    


@cli.command(help= 'view my company logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_my_company_logs(output_file):
    view_my_logs_sk(output_file,False,True)


@cli.command(help='view my encrypted logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs; view in terminal if not provided')
def view_my_encrypted_logs(output_file):
    decrypted_logs = view_my_logs_sk(output_file, True, False)
    
    
    for encrypted_log in decrypted_logs:
        print(encrypted_log[0])
       
        encrypted_hex, nonce, tag =encrypted_log[0].split('.')
        decrypted_data = aesDecrypt(encrypted_hex, getAESKey(my_wallet_address()), nonce, tag)
        print(decrypted_data)

    

    ##tutaj jeszcze zapis  do  pliku

#zapis do pliku oraz w jaki sposob klucz publiczny i prywatny dodoac
@cli.command(help= 'view my company logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_my_encrypted_company_logs(output_file):
    encrypted_logs=view_my_logs_sk(output_file,True,True)
    
    private_key = get_private_key(my_wallet_address())

    decrypted_logs = []
    for encrypted_log in encrypted_logs:
        log = encrypted_log[0]
        log_data_bytes = bytes.fromhex(log)
        decrypted_log = rsaDecrypt(log_data_bytes, private_key)
        print(decrypted_log)
        
        
        

#############################################################################
#############################################################################
#viewUserLogs

@cli.command(help= 'view user logs')
@click.option('--user_address', help='User address')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_user_logs(user_address,output_file):
        view_user_logs_sk(user_address,output_file,False,False)
    



@cli.command(help= 'view user company logs')
@click.option('--user_address', help='User address')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_user_company_logs(user_address,output_file):
    view_user_logs_sk(user_address,output_file,False,True)



@cli.command(help= 'view user  encrypted logs')
@click.option('--user_address', help='User address')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_user_encrypted_logs(user_address,output_file):
        decrypted_logs=view_user_logs_sk(user_address,output_file,True,False)
        
        decrypted_logs = []
        for encrypted_log in decrypted_logs:
            encrypted_hex, nonce, tag =encrypted_log[0].split('.')
            decrypted_data = aesDecrypt(encrypted_hex, getAESKey(user_address), nonce, tag)
            print(decrypted_data)

    


@cli.command(help= 'view user company  encrypted logs')
@click.option('--user_address', help='User address')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_user_encrypted_company_logs(user_address,output_file):
    encrypted_logs=view_user_logs_sk(user_address,output_file,True,True)
    private_key = get_private_key(user_address)

    decrypted_logs = []
    for encrypted_log in encrypted_logs:
        log = encrypted_log[0]
        log_data_bytes = bytes.fromhex(log)
        decrypted_log = rsaDecrypt(log_data_bytes, private_key)
        
        print(decrypted_log)
        

 

#############################################################################




######################################################################################

#AddLogs

@cli.command(help='Add log entry for a user')
@click.option('--log_data', help='Log data to add')
def add_log( log_data):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()


    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'addUserLog', [log_data], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('Log entry added succesfully')


@cli.command(help='my wallet address ')
def my_address():
    print(my_wallet_address())

@cli.command(help='Add log encrypted entry ')
@click.option('--log_data', help='Log data to add')
def add_encrypted_log(log_data):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
    key = getAESKey(my_wallet_address())
    
    
    log_data_bytes = log_data.encode()
    
    encrypted_hex, nonce, tag = aesEncrypt(log_data_bytes, key)

    result = ".".join([encrypted_hex, nonce, tag])  
    
    receipt = execute_transaction(
        contract, 'addEncryptedUserLog', [result], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print(encrypted_hex)
        print('Log entry added successfully')

     
   
@cli.command(help='Add company log entry for a user Admin or superuserOnly')
@click.option('--user_address', help='User address')
@click.option('--log_data', help='Log data to add')
def add_company_log(user_address, log_data):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()

    
    receipt = execute_transaction(
        contract, 'addCompanyLog', [user_address, log_data], chain_id, wallet_address, private_key, web3
    )

    if receipt.status == 1:
        print('Company log entry added successfully')



@cli.command(help='Add encrypted company log entry for a user Admin or superuserOnly')
@click.option('--user_address', help='User address')
@click.option('--log_data', help='Log data to add')
def add_encrypted_company_log(user_address, log_data):
    contract, wallet_address, private_key, chain_id, web3 = get_contract_and_credentials()
    public_key = get_public_key(user_address)
    
    
    log_data_bytes = log_data.encode()
    
    log_data_encrypted = rsaEncrypt(log_data_bytes, public_key)
    
    
    log_data_hex = log_data_encrypted.hex()
    
    receipt = execute_transaction(
        contract, 'addEncryptedCompanyLog', [user_address, log_data_hex], chain_id, wallet_address, private_key, web3
    )

    if receipt.status == 1:
        print(log_data_hex)
        print('Company log entry added successfully')




@cli.command(help=' ONLYADMIN OR SUPERUSER Add piblic log entry' )
@click.option('--log_data', help='Log data to add')
def add_public_log( log_data):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'addPublicLog', [log_data], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print("Log entry added successfully")

###new admin add code

@cli.command(help= 'view public logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_public_logs(output_file):

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    my_logs = contract.functions.getPublicLogs().call({'from': wallet_address})
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write("Public Logs:\n")
            for my_log in my_logs:
                f.write(str(my_log) + '\n')
        print(f"Your logs saved to {output_file}")
    else:
        print("PUBLIC Logs:")
        for my_log in my_logs:
            print(my_log)


######################################################################################

if __name__ == '__main__':
    cli()

import click
import json
from web3 import Web3
from hexbytes import HexBytes

@click.group()
@click.pass_context
def cli(ctx):
    pass


#can be only 1 admin
#loginadmin


#help function
def load_config():
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        print("config file problem")
        return None

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

# init change?
@cli.command(help='Initialization')
@click.option('--wallet_address', help='Your wallet address ')
@click.option('--private_key', help='Your private key.')

def init(wallet_address, private_key): 
    if not wallet_address or not private_key:
        print("Error: Please provide both wallet address and private key.")
        return
    

    sepolia_rpc_url = "https://sepolia.base.org"
    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    print(f"Is connected: {web3.is_connected()}")  # Is connected: True
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)

    chain_id = web3.eth.chain_id
    contract_address = '0x9dE15036DF84FdF8ad19E5ba0fb4aE62E4a41F98'
    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi) 
    print(contract)
    config_data = {
        'wallet_address': wallet_address,
        'private_key': private_key,
        'chain_id': chain_id,
        'contract_address': contract_address,
        'sepolia_rpc_url' : "https://sepolia.base.org"
    }
    with open('config.json', 'w') as file:
        json.dump(config_data, file)



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


#problem
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
     


@cli.command(help='Add log entry for a user')
@click.option('--log_data', help='Log data to add')
def add_log( log_data):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()

   

    # Wywołanie uniwersalnej metody execute_transaction
    receipt = execute_transaction(
        contract, 'addLog', [log_data], chain_id, wallet_address, private_key, web3
    )

    print(receipt)
    if receipt.status == 1:
        print('Log entry added succesfully')
     
   

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

@cli.command(help = 'adminOnly add new superuser')
@click.option('--address', help='New admin address')

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


@cli.command(help='Admin OR SUPERUSER Only get another user logs')
@click.option('--user_address', help='User address')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def get_user_logs(user_address, output_file):
    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
     
    user_logs = contract.functions.getUserLogs(user_address).call({'from': wallet_address})
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write("User Logs:\n")
            for user_log in user_logs:
                f.write(str(user_log) + '\n')
        print(f"User logs saved to {output_file}")
    else:
        print("User Logs:")
        for user_log in user_logs:
            print(user_log)



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




@cli.command(help= 'view my logs')
@click.option('-f', '--file', 'output_file', type=click.Path(), help='File to save logs see in terminal without this function')
def view_my_logs(output_file):

    contract, wallet_address, private_key,chain_id,web3 = get_contract_and_credentials()
    my_logs = contract.functions.viewMyLogs().call({'from': wallet_address})
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write("My Logs:\n")
            for my_log in my_logs:
                f.write(str(my_log) + '\n')
        print(f"Your logs saved to {output_file}")
    else:
        print("My Logs:")
        for my_log in my_logs:
            print(my_log)



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

if __name__ == '__main__':
    cli()

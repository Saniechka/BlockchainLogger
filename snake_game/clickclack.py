import click
import json
from web3 import Web3
from hexbytes import HexBytes

@click.group()
@click.pass_context
def cli(ctx):
    pass
#can be only 1 admin

#TODO     add logs to file  bug in details function 



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
     

    return contract, wallet_address, private_key





# init change?
@cli.command(help='Initialization')
@click.option('--wallet_address', help='Your wallet address ')
@click.option('--private_key', help='Your private key.')

def init(wallet_address, private_key): 
    

    sepolia_rpc_url = "https://sepolia.base.org"
    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    print(f"Is connected: {web3.is_connected()}")  # Is connected: True
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)

    chain_id = web3.eth.chain_id
    contract_address = '0x079296643e39A7E5e872ba9a76c8d4E138F00209'
    
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

    contract, wallet_address, private_key = get_contract_and_credentials()
     


    transaction = contract.functions.registerUser(
        address, login, password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status == 1 :
        print('OK')

#problem
@cli.command()
@click.option('--address', help='User address')
def getUserDetails( address):
    contract, wallet_address, private_key = get_contract_and_credentials()
    
    result = contract.functions.getUserDetails(address).call({'from': wallet_address})

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
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.setAdmin(address).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    print("ok")


@cli.command(help='Add log entry for a user')
@click.option('--log_data', help='Log data to add')
def add_log( log_data):
    contract, wallet_address, private_key = get_contract_and_credentials()
     
   
    transaction = contract.functions.addLog(log_data).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status == 1:
        print("Log entry added successfully")



@cli.command(help = 'adminOnly add new superuser')
@click.option('--address', help='New admin address')

def set_SuperUser(address):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.setSuperuser(address).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    print("ok")



@cli.command(help= 'adminOnly change another user password')
@click.option('--address', help='User address')
@click.option('--new_password', help='New password')

def change_user_password( address, new_password):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.changeUserPassword(
        address, new_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status ==1:
        print('OK')


@cli.command(help='adminOnly change another user name')
@click.option('--address', help='User address')
@click.option('--new_name', help='New user name')
def change_user_name(address, new_name):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.changeUserName(
        address, new_name
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if  receipt.status == 1: 
        print('OK')


@cli.command(help = 'change password')
@click.option('--new_password', help='New password')

def change_my_password(new_password):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.changeMyPassword(
        new_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status == 1:
        print("password changing succes")


@cli.command(help = 'comand for logging')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
def login(user_login, user_password):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.loginUser(
         user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status == 1:
        print("loging succes")


@cli.command(help ='log out')
def logout( ):
    contract, wallet_address, private_key = get_contract_and_credentials()
     

    transaction = contract.functions.logoutUser(
         
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    if receipt.status == 1:
        print("logout succes")



@cli.command(help = 'AdminOnly get anotheruser logs')
@click.option('--user_address', help='User address')
def get_user_logs(user_address):
    contract, wallet_address, private_key = get_contract_and_credentials()
     
    user_logs = contract.functions.getLogs(user_address,).call({'from': wallet_address})
    
    print("User Logs:")
    for user_log in user_logs:
        print(user_log)



@cli.command(help= 'onlyAdmin get list of all users')
def get_all_users():

    contract, wallet_address, private_key = get_contract_and_credentials()
     
    users = contract.functions.getAllUsers().call({'from': wallet_address})

    print("List of all users:")
    for user_address in users:
        print(user_address)



@cli.command(help= 'See my status')
def view_my_role( ):
    
    contract, wallet_address, private_key = get_contract_and_credentials()
     
    user_status = contract.functions.viewUserStatus().call({'from': wallet_address})
    
    print(user_status)



@cli.command(help= 'view my logs')
def view_my_logs():

    contract, wallet_address, private_key = get_contract_and_credentials()
    my_logs = contract.functions.viewMyLogs().call({'from': wallet_address})
    
    print("My Logs:")
    for log in my_logs:
        print(log)



@cli.command(help = 'see admin addres')
def adminAddres():
    
    contract, wallet_address, private_key = get_contract_and_credentials()
    admin_address = contract.functions.adminAddress().call({'from': wallet_address})

    print("AdminAddres:", admin_address)



@cli.command(help = 'see admin addres')
def superuserAddres():

    contract, wallet_address, private_key = get_contract_and_credentials()
     
    superuser_address = contract.functions.superuserAddress().call({'from': wallet_address})

    print("superuserAddres:", admin_address)



@cli.command(help= 'adminOnly check user role')
@click.option('--address', help='User address')
def check_User_Role(address):
    contract, wallet_address, private_key = get_contract_and_credentials()
    address = Web3.to_checksum_address(address)
    user_status = contract.functions.checkUserStatus(address).call({'from': wallet_address})

    print("User status:", user_status)

@cli.command(help= 'check if user logged')
@click.option('--address', help='User address')
def is_User_Logged_In( address):

    contract, wallet_address, private_key = get_contract_and_credentials()
    is_logged_in = contract.functions.isUserLoggedIn(address).call({'from': wallet_address})
    
    print("Is user logged in:", is_logged_in)

if __name__ == '__main__':
    cli()

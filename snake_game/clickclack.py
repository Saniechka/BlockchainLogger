import click
import json
from web3 import Web3

@click.group()
@click.pass_context
def cli(ctx):
    pass



def load_config():
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        print("Конфигурационный файл не найден. Пожалуйста, запустите команду 'init' сначала.")
        return None

@cli.command()
@click.option('--wallet_address', help='Your wallet address ')
@click.option('--private_key', help='Your private key.')
@click.pass_context
def init(ctx, wallet_address, private_key): 
    

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




    
# Команда для регистрации нового пользователя
@cli.command()
@click.option('--address', help='New user address')
@click.option('--login', help='New user login')
@click.option('--password', help='New user password')
@click.pass_context
def register_user(address, login, password):

    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url)) 
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address


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


@cli.command()
@click.option('--address', help='User address')
@click.pass_context
def getUserDetails(ctx, address):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    user_details = contract.functions.getUserDetails(address).call()
    print("User details:", user_details)


@cli.command()
@click.option('--address', help='User address')
@click.pass_context
def checkUserStatus(ctx, address):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    user_status = contract.functions.checkUserStatus(address).call()
    print("User status:", user_status)


@cli.command()
@click.option('--address', help='User address')
@click.pass_context
def isUserLoggedIn(ctx, address):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    is_logged_in = contract.functions.isUserLoggedIn(address).call()
    print("Is user logged in:", is_logged_in)


@cli.command()
@click.option('--address', help='New admin address')
@click.pass_context
def setAdmin(ctx, address):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

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



@cli.command()
@click.option('--address', help='User address')
@click.option('--new_password', help='New password')
@click.pass_context
def change_user_password(ctx, address, new_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.changeUserPassword(
        address, new_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)


@cli.command()
@click.option('--address', help='User address')
@click.option('--new_name', help='New user name')
@click.pass_context
def change_user_name(ctx, address, new_name):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.changeUserName(
        address, new_name
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)


@cli.command()
@click.option('--new_password', help='New password')
@click.pass_context
def change_my_password(ctx, new_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.changeMyPassword(
        new_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)


@cli.command()
@click.option('--user_address', help='User address')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
@click.pass_context
def login_user(ctx, user_address, user_login, user_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.loginUser(
        user_address, user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)


@cli.command()
@click.option('--user_address', help='User address')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
@click.pass_context
def logout_user(ctx, user_address, user_login, user_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.logoutUser(
        user_address, user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)



@cli.command()
@click.option('--user_address', help='User address')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
@click.pass_context
def get_logs(ctx, user_address, user_login, user_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.getLogs(
        user_address, user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)


@cli.command()
@click.option('--user_address', help='User address')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
@click.pass_context
def get_all_users(ctx, user_address, user_login, user_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.getAllUsers(
        user_address, user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)




@cli.command()
@click.option('--user_address', help='User address')
@click.option('--user_login', help='User login')
@click.option('--user_password', help='User password')
@click.pass_context
def view_user_status(ctx, user_address, user_login, user_password):
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url = config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    transaction = contract.functions.viewUserStatus(
        user_address, user_login, user_password
    ).build_transaction({
        'chainId': chain_id,
        'gas': 1000000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)





@cli.command()
def viewMyLogs():

    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url)) 
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    my_logs = contract.functions.viewMyLogs().call()
    print(my_logs)


@cli.command()
def adminAddres():

    with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)
    config_data = load_config()
    if config_data is None:
        return

    wallet_address = config_data['wallet_address']
    private_key = config_data['private_key']
    chain_id = config_data['chain_id']
    contract_address = config_data['contract_address']
    sepolia_rpc_url= config_data['sepolia_rpc_url']

    web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url)) 
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    web3.eth.default_account = wallet_address

    admin_address = contract.functions.adminAddress().call()

    print("AdminAddres:", admin_address)

if __name__ == '__main__':
    cli()

from web3 import Web3
from eth_account import Account
import json


'https://eth-sepolia.g.alchemy.com/v2/demo'
# URL конечной точки Infura
infura_url = 'https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'
w3 = Web3(Web3.HTTPProvider(infura_url))

# ABI вашего контракта
contract_abi = json.loads('YOUR_CONTRACT_ABI')

# Адрес вашего контракта
contract_address = 'YOUR_CONTRACT_ADDRESS'

# Создание экземпляра контракта
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Пример вызова функции контракта
# Замените 'functionName' на имя функции, которую вы хотите вызвать
result = contract.functions.functionName().call()
print(result)
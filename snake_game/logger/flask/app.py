
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import hashlib
from web3 import Web3
import json




file_path = "variable.json"
with open('contract_abi.json', 'r') as file:
        contract_abi = json.load(file)


with open(file_path, "r") as file:
    data1 = json.load(file)

sepolia_rpc_url = data1["sepolia_rpc_url"]
web3 = Web3(Web3.HTTPProvider(sepolia_rpc_url))

chain_id = web3.eth.chain_id
contract_address = data1["contract_address"] #wpisac jako zmienna
contract = web3.eth.contract(address=contract_address, abi=contract_abi) 
   
def get_filed_data_frontend(file_hash):
    if not file_hash:
        print("Error: Please provide the file hash.")
        return


     
    file_data = contract.functions.get(file_hash).call()
    if file_data[5]==True:
        
        return True
    return False

    '''
    print("File Hash:", file_data[0])
    print("IPFS Hash:", file_data[1])
    print("File Name:", file_data[2])
    print("File Type:", file_data[3])
    print("Date Added:", file_data[4])
    print("Exist:", file_data[5])
    '''


app = Flask(__name__)

# Konfiguracja katalogu do przechowywania plików
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dozwolone rozszerzenia plików
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_file_hash(file_path):
    """Oblicz hash SHA-256 pliku."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Oblicz hash pliku
        file_hash = calculate_file_hash(file_path)
        data = get_filed_data_frontend(file_hash)
        if data:
            return "True"

        return "False" 
        
        #return f'File successfully uploaded. SHA-256 hash: {file_hash}'
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)



'''
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import hashlib

app = Flask(__name__)

# Konfiguracja katalogu do przechowywania plików
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dozwolone rozszerzenia plików
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_file_hash(file_path):
    """Oblicz hash SHA-256 pliku."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Oblicz hash pliku
        file_hash = calculate_file_hash(file_path)
        
        return f'File successfully uploaded. SHA-256 hash: {file_hash}'
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)
'''

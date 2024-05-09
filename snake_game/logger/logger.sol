// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;


contract Auth {

    address public adminAddress;
    address public superuserAddress;

    enum UserRole { Admin, Superuser, User }

    struct UserDetail {
    string name;
    string password;
    bool isUserLoggedIn;
    UserRole role;
    bool isSuperuser; 
}


    struct DocInfo { 
        string ipfsHash; 
        string fileName; 
        string fileType; 
        uint dateAdded; 
        bool exist;  
    }

    mapping (string => DocInfo) collection; 
    mapping(address => UserDetail) public users;
    address[] public userList;
    
    

    struct LogEntry {
        string logData;
        bool isEncrypted; // Informacja czy log jest zaszyfrowany
        bool isCompanyLog; // Informacja czy log jest od firmy
    }

    
    mapping(address => LogEntry[]) public allLogs;
    LogEntry[] public publicLogs;

    event UserRegistered(address indexed userAddress, string name, bool isUserLoggedIn);
    event UserPasswordChanged(address indexed userAddress, string newPassword);
    event UserNameChanged(address indexed userAddress, string newName);
    event UserLoggedIn(address indexed userAddress);
    event UserLoggedOut(address indexed userAddress);
    event LogAdded(address indexed userAddress, string logData);
    event HashAdded(string ipfsHash, string fileHash, uint dateAdded);

    constructor() {
        adminAddress = msg.sender;
        superuserAddress = address(0); 
        registerUser(msg.sender, "admin", "admin");
    }

    modifier onlyAdmin() {
        require(msg.sender == adminAddress, "Only admin can call this function");
        _;
    }

    modifier onlyAdminOrSuperuser() {
        require(msg.sender == adminAddress || msg.sender == superuserAddress, "Only admin or superuser can call this function");
        _;
    }

     modifier onlyUser() {
    require(bytes(users[msg.sender].name).length > 0, "Only registered users can call this function");
    require(users[msg.sender].isUserLoggedIn, "User must be logged in");
    _;
}


// Funkcja dodająca logi
    // Dodawanie logu firmy
function addCompanyLog(address _userAddress, string memory _logData) public onlyAdminOrSuperuser {
    allLogs[_userAddress].push(LogEntry({
        logData: _logData,
        isEncrypted: false,
        isCompanyLog: true
    }));
}

// Dodawanie zaszyfrowanego logu firmy
function addEncryptedCompanyLog(address _userAddress, string memory _logData) public onlyAdminOrSuperuser {
    allLogs[_userAddress].push(LogEntry({
        logData: _logData,
        isEncrypted: true,
        isCompanyLog: true
    }));
}

// Dodawanie zaszyfrowanego logu użytkownika
function addEncryptedUserLog( string memory _logData) public onlyUser onlyAdminOrSuperuser {
    allLogs[msg.sender].push(LogEntry({
        logData: _logData,
        isEncrypted: true,
        isCompanyLog: false
    }));
}

// Dodawanie zwykłego logu użytkownika
function addUserLog( string memory _logData) public onlyUser {
    allLogs[msg.sender].push(LogEntry({

        logData: _logData,
        isEncrypted: false,
        isCompanyLog: false
    }));
}


function addPublicLog(string memory _logData) public  onlyUser  onlyAdminOrSuperuser {
    publicLogs.push(LogEntry({
        logData: _logData,
        isEncrypted: false,
        isCompanyLog: false
    }));
}



    function getPublicLogs() public view returns (string[] memory) {
    uint256 logsCount = publicLogs.length;
    string[] memory logStrings = new string[](logsCount);

    for (uint256 i = 0; i < logsCount; i++) {
        logStrings[i] = publicLogs[i].logData;
    }

    return logStrings;
}
    function getUserDetails(address _userAddress) public view onlyUser onlyAdmin returns (string memory) {
        UserDetail memory user = users[_userAddress];
        string memory userDetails = string(abi.encodePacked(user.name, ",", user.password, ",", user.isUserLoggedIn ? "true" : "false", ",", userRoleToString(user.role)));
        return userDetails;
    }


function add(string memory _ipfsHash, string memory _fileHash, string memory _fileName, string memory _fileType, uint _dateAdded) public onlyAdminOrSuperuser { 
        require(collection[_fileHash].exist == false, "[E1] This hash already exists in contract."); 
        DocInfo memory docInfo = DocInfo(_ipfsHash, _fileName, _fileType, _dateAdded, true); 
        collection[_fileHash] = docInfo; 

        emit HashAdded(_ipfsHash, _fileHash, _dateAdded); 
    } 

    function get(string memory _fileHash) public view returns (string memory, string memory, string memory, string memory, uint, bool) { 
        return ( 
            _fileHash,  
            collection[_fileHash].ipfsHash, 
            collection[_fileHash].fileName, 
            collection[_fileHash].fileType, 
            collection[_fileHash].dateAdded, 
            collection[_fileHash].exist 
        ); 
    } 

   

    function userRoleToString(UserRole role) private pure returns (string memory) {
        if (role == UserRole.Admin) {
            return "Admin";
        } else if (role == UserRole.Superuser) {
            return "Superuser";
        } else {
            return "User";
        }
    }


//userrole
    function checkUserRole(address _userAddress) public view onlyUser onlyAdmin returns (string memory) {
    UserDetail memory user = users[_userAddress];
    require(bytes(user.name).length > 0, "User is not registered");
    if (_userAddress == adminAddress) {
        return "Admin";
    } else if (_userAddress == superuserAddress) {
        return "Superuser";
    } else if (user.isSuperuser) {
        return "Superuser";
    } else {
        return "User";
    }
}


function isUserLoggedIn(address _userAddress) public view  onlyUser onlyAdmin  returns (bool) {
    UserDetail memory user = users[_userAddress];
    require(bytes(user.name).length > 0, "User is not registered");
    return user.isUserLoggedIn;
}



  

    function setSuperuser(address _superuserAddress) public onlyUser onlyAdmin {
        superuserAddress = _superuserAddress;
    }

    function setAdmin(address _adminAddress) public onlyUser onlyAdmin {
        adminAddress = _adminAddress;
    }

    function registerUser(
    address _userAddress,
    string memory _name,
    string memory _password
) public onlyAdmin returns (bool) {
    require(bytes(users[_userAddress].name).length == 0, "User already registered");
    users[_userAddress].name = _name;
    users[_userAddress].password = _password;
    users[_userAddress].isUserLoggedIn = false;
    users[_userAddress].role = UserRole.User; 
    users[_userAddress].isSuperuser = false; 
    userList.push(_userAddress);
    emit UserRegistered(_userAddress, _name, false);
    return true;
}




    function changeUserPassword(address _userAddress, string memory _newPassword) public onlyUser onlyAdmin {
        users[_userAddress].password = _newPassword;
        emit UserPasswordChanged(_userAddress, _newPassword);
    }

    function changeUserName(address _userAddress, string memory _newName) public onlyUser onlyAdmin {
        
        users[_userAddress].name = _newName;
        emit UserNameChanged(_userAddress, _newName);
    }



    function changeMyPassword(string memory _newPassword) public onlyUser {
    
    users[msg.sender].password = _newPassword;
    emit UserPasswordChanged(msg.sender, _newPassword);
}


   
//login
   function login(string memory _name, string memory _password) public returns (bool) {
    require(bytes(users[msg.sender].name).length > 0, "User is not registered");
    require(keccak256(abi.encodePacked(users[msg.sender].name)) == keccak256(abi.encodePacked(_name)), "Invalid name");
    require(keccak256(bytes(users[msg.sender].password)) == keccak256(bytes(_password)), "Invalid password");
    users[msg.sender].isUserLoggedIn = true;
    emit UserLoggedIn(msg.sender);
    return true;
}

    function logoutUser() public onlyUser {
        users[msg.sender].isUserLoggedIn = false;
        emit UserLoggedOut(msg.sender);
    }




   // Funkcja pobierająca określony rodzaj logów użytkownika
function getUserLogs(address _userAddress, bool _isEncrypted, bool _isCompanyLog) public onlyAdminOrSuperuser view returns (LogEntry[] memory) {
    LogEntry[] memory userLogs = allLogs[_userAddress];
    LogEntry[] memory filteredLogs = new LogEntry[](userLogs.length);
    uint256 filteredLogsCount = 0;

    for (uint256 i = 0; i < userLogs.length; i++) {
        if (userLogs[i].isEncrypted == _isEncrypted && userLogs[i].isCompanyLog == _isCompanyLog) {
            filteredLogs[filteredLogsCount] = userLogs[i];
            filteredLogsCount++;
        }
    }

    // Tworzenie nowej tablicy o odpowiedniej długości
    LogEntry[] memory resultLogs = new LogEntry[](filteredLogsCount);
    for (uint256 j = 0; j < filteredLogsCount; j++) {
        resultLogs[j] = filteredLogs[j];
    }

    return resultLogs;
}

function getMyLogs(bool _isEncrypted, bool _isCompanyLog) public onlyUser view returns (LogEntry[] memory) {
    LogEntry[] memory userLogs = allLogs[msg.sender];
    LogEntry[] memory filteredLogs = new LogEntry[](userLogs.length);
    uint256 filteredLogsCount = 0;

    for (uint256 i = 0; i < userLogs.length; i++) {
        if (userLogs[i].isEncrypted == _isEncrypted && userLogs[i].isCompanyLog == _isCompanyLog) {
            filteredLogs[filteredLogsCount] = userLogs[i];
            filteredLogsCount++;
        }
    }

    // Tworzenie nowej tablicy o odpowiedniej długości
    LogEntry[] memory resultLogs = new LogEntry[](filteredLogsCount);
    for (uint256 j = 0; j < filteredLogsCount; j++) {
        resultLogs[j] = filteredLogs[j];
    }

    return resultLogs;
}


//see my userrole
    function viewMyRole() public view onlyUser returns (string memory) {
        if (msg.sender == adminAddress) {
            return "Admin";
        } else if (msg.sender == superuserAddress) {
            return "Superuser";
        } else {
            return "User";
        }
    }
}
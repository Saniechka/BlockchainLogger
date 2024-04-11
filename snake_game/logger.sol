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
    bool isSuperuser; // Добавлено поле isSuperuser
}


    mapping(address => UserDetail) public users;
    address[] public userList;

    struct LogEntry {
        string logData;
    }

    mapping(address => LogEntry[]) public logs;

    event UserRegistered(address indexed userAddress, string name, bool isUserLoggedIn);
    event UserPasswordChanged(address indexed userAddress, string newPassword);
    event UserNameChanged(address indexed userAddress, string newName);
    event UserLoggedIn(address indexed userAddress);
    event UserLoggedOut(address indexed userAddress);

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

    function getUserDetails(address _userAddress) public view onlyAdmin returns (string memory name,string memory password, bool isLoggedIn, string memory role) {
        UserDetail memory user = users[_userAddress];
        return (user.name,user.password, user.isUserLoggedIn, userRoleToString(user.role));
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



    function checkUserStatus(address _userAddress) public view onlyAdmin returns (string memory) {
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


function isUserLoggedIn(address _userAddress) public view returns (bool) {
    UserDetail memory user = users[_userAddress];
    require(bytes(user.name).length > 0, "User is not registered");
    return user.isUserLoggedIn;
}



   modifier onlyUser() {
    require(bytes(users[msg.sender].name).length > 0, "Only registered users can call this function");
    require(users[msg.sender].isUserLoggedIn, "User must be logged in");
    _;
}

    function setSuperuser(address _superuserAddress) public onlyAdmin {
        superuserAddress = _superuserAddress;
    }

    function setAdmin(address _adminAddress) public onlyAdmin {
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
    users[_userAddress].role = UserRole.User; // Установка роли пользователя
    users[_userAddress].isSuperuser = false; // Установка isSuperuser в false по умолчанию
    userList.push(_userAddress);
    emit UserRegistered(_userAddress, _name, false);
    return true;
}

    function changeUserPassword(address _userAddress, string memory _newPassword) public onlyAdmin {
        require(_userAddress == msg.sender, "Only the user can change their password");
        users[_userAddress].password = _newPassword;
        emit UserPasswordChanged(_userAddress, _newPassword);
    }

    function changeUserName(address _userAddress, string memory _newName) public onlyAdmin {
        
        users[_userAddress].name = _newName;
        emit UserNameChanged(_userAddress, _newName);
    }



    function changeMyPassword(string memory _newPassword) public onlyUser {
    // Использует msg.sender для идентификации пользователя, который вызывает функцию
    users[msg.sender].password = _newPassword;
    emit UserPasswordChanged(msg.sender, _newPassword);
}


   

   function loginUser(string memory _name, string memory _password) public returns (bool) {
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

    function addLog(string memory _logData) public onlyUser {
        logs[msg.sender].push(LogEntry({
            logData: _logData
        }));
    }

    function getLogs(address _userAddress) public view returns (LogEntry[] memory) {
        return logs[_userAddress];
    }

    function getAllUsers() public view onlyAdmin returns (address[] memory) {
        return userList;
    }

    function viewMyLogs() public view onlyUser returns (LogEntry[] memory) {
    return getLogs(msg.sender);
}

    function viewUserStatus() public view onlyUser returns (string memory) {
        if (msg.sender == adminAddress) {
            return "Admin";
        } else if (msg.sender == superuserAddress) {
            return "Superuser";
        } else {
            return "User";
        }
    }
}

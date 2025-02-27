//MIT Licensed[soon]: Feel free to use for anything!
pragma solidity ^0.8.0;

contract ContractorFileStorage {

    constructor(){}
    fallback() external payable {}
    receive() external payable {}
    struct FileData {
        address payable client;
        address payable storageProvider;
        uint256 startTime;
        uint256 duration; // in hours, max 30 days (720 hours)
        uint256 storageSpace; // in bytes
        uint256 totalAmount;
        uint256 remainingAmount;
        uint256 lastValidationTime;
        bool isActive;
        bool isApproved;
    }

    // Constants
    uint256 public constant MAX_DURATION = 720 hours; // 30 days
    uint256 public constant VALIDATION_INTERVAL = 2 ; // blocks
    uint256 public constant PRICE_PER_GB_PER_HOUR = 1 wei;

    // Storage
    // FileID=>FileData
    mapping(bytes32 => FileData) public files;


    // Events
    event DealProposed(bytes32 indexed fileId, address indexed client, uint256 space, uint256 duration);
    event DealApproved(bytes32 indexed fileId, address indexed storageProvider);
    event ProofValidated(bytes32 indexed fileId, uint256 timestamp);
    event DealInvalidated(bytes32 indexed fileId, string reason);
    event DealCompleted(bytes32 indexed fileId);

    modifier onlyClient(bytes32 fileId) {
        require(files[fileId].client == msg.sender, ";;onlyClient;; : Only client can call this");
        _;
    }

    modifier dealActive(bytes32 fileId) {
        require(files[fileId].isActive, ";;dealActive;; : Deal is not active");
        _;
    }

    function proposeDeal(
        bytes32 fileId,
        uint256 storageSpace,
        uint256 durationBlocks
    ) external payable  {
        require(durationBlocks <= MAX_DURATION, "[proposeDeal]: Duration exceeds maximum limit");
        require(storageSpace > 0, "[proposeDeal]: Storage space must be positive");
        require(files[fileId].client == address(0), "[proposeDeal]: File ID already exists");
        uint256 totalAmount = calculateTotalAmount(storageSpace, durationBlocks);

        require(msg.value==totalAmount, "[proposeDeal]: Incorrect balance to propose a deal");

        files[fileId] =  FileData({
            client: payable(msg.sender),
            storageProvider: payable(address(0)),
            startTime: 0,
            duration: durationBlocks,
            storageSpace: storageSpace,
            totalAmount: totalAmount,
            remainingAmount: totalAmount,
            lastValidationTime: 0,
            isActive: false,
            isApproved: false
        });

        emit DealProposed(fileId, msg.sender, storageSpace, durationBlocks);

    }
    function completeDeal(bytes32 fileId) public  {
        require(files[fileId].client != address(0), "[completedeal]: File does not exist");
        require(files[fileId].isActive, "[completedeal]: Deal is not active");

//        FileData storage file = files[fileId];
        files[fileId].isActive = false;

//        if (files[fileId].remainingAmount > 0) {
//            require(files[fileId].storageProvider != address(0), "[completedeal]: Invalid storage provider address");
//
//            payable(files[fileId].storageProvider).transfer(files[fileId].remainingAmount);
//        }
        delete files[fileId];

        emit DealCompleted(fileId);
    }
    function approveDeal(bytes32 fileId, uint256 billingAmount) external payable {
        require(!files[fileId].isApproved, "[approveDeal]: Deal already approved");
        require(files[fileId].client != address(0), "[approveDeal]: Deal does not exist");
        require(billingAmount * 1 wei == files[fileId].totalAmount, "[approveDeal]: Mismatch between two prices!");
        require(files[fileId].client != msg.sender, "[approveDeal]: Only server can approve the deal");

        files[fileId].storageProvider = payable(msg.sender);
        files[fileId].startTime = block.number;
        files[fileId].lastValidationTime = block.number;
        files[fileId].isActive = true;
        files[fileId].isApproved = true;

        emit DealApproved(fileId, msg.sender);
    }


    function validateProof(bytes32 fileId) external payable dealActive(fileId) onlyClient(fileId) dealActive(fileId)  {
//        FileData storage file = files[fileId];
        require(files[fileId].client != address(0), "[validateProof]: File does not exist");
//        require(block.number >= 1 + files[fileId].lastValidationTime, "[validateProof]: Too early for validation");
        require(files[fileId].storageProvider != address(0), "[validateProof]: Invalid storage provider address");

        uint256 payment = (files[fileId].totalAmount)/files[fileId].duration;
        files[fileId].remainingAmount -= payment;
        files[fileId].lastValidationTime = block.number;

        payable(files[fileId].storageProvider).transfer(payment);

        emit ProofValidated(fileId, block.timestamp);
        // return payment;
    }

    function invalidateDeal(bytes32 fileId, string memory reason) external payable onlyClient(fileId) dealActive(fileId) {
//        FileData storage file = files[fileId];
        require(files[fileId].client != address(0), "[invalidateProof]: File does not exist");
        require(files[fileId].isActive, "[invalidateProof]: Deal is not active");
        require(msg.sender == files[fileId].client, "[invalidateProof]: Only the client can invalidate the deal");

        payable(files[fileId].client).transfer(files[fileId].remainingAmount);
        delete files[fileId]; // render everything useless
//        files[fileId].isActive = false;
        emit DealInvalidated(fileId, reason);
    }



    function calculateTotalAmount(uint256 storageSpace, uint256 durationHours) public pure returns (uint256) {
        uint256 spaceInGB = storageSpace ;
        return spaceInGB * durationHours * 1 wei;
    }


    function getFileData(bytes32 fileId) public view returns (FileData memory) {
        return files[fileId];  // Return the FileData struct for the given fileId
    }
    function getBalance() public view returns (uint256) {
        return address(this).balance;
}

}
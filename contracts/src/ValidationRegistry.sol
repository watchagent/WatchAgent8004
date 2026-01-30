// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ValidationRegistry
 * @dev ERC-8004 Validation Registry - Cryptoeconomic validation mechanism
 * @notice Manages validation requests and responses for agent work
 */
contract ValidationRegistry {
    struct ValidationRequest {
        uint256 agentId;
        address requester;
        uint256 validatorId;
        string requestURI; // IPFS link to validation request data
        bytes32 requestHash;
        uint256 timestamp;
        bool completed;
    }
    
    struct ValidationResponse {
        uint256 requestId;
        uint256 validatorId;
        uint8 score; // 0-100
        string responseURI; // IPFS link to validation response
        bytes32 responseHash;
        uint256 timestamp;
    }
    
    // Request ID => ValidationRequest
    mapping(uint256 => ValidationRequest) public validationRequests;
    
    // Request ID => ValidationResponse
    mapping(uint256 => ValidationResponse) public validationResponses;
    
    // Agent ID => Request IDs
    mapping(uint256 => uint256[]) public agentValidationRequests;
    
    // Validator ID => Request IDs
    mapping(uint256 => uint256[]) public validatorRequests;
    
    uint256 public totalRequests;
    
    event ValidationRequested(
        uint256 indexed requestId,
        uint256 indexed agentId,
        uint256 indexed validatorId,
        address requester,
        uint256 timestamp
    );
    
    event ValidationResponseSubmitted(
        uint256 indexed requestId,
        uint256 indexed validatorId,
        uint8 score,
        uint256 timestamp
    );
    
    /**
     * @dev Request validation from a validator
     * @param agentId Agent requesting validation
     * @param validatorId Validator to perform validation
     * @param requestURI URI to validation request data
     * @param requestHash Hash of request data
     * @return requestId The ID of the validation request
     */
    function requestValidation(
        uint256 agentId,
        uint256 validatorId,
        string memory requestURI,
        bytes32 requestHash
    ) external returns (uint256) {
        require(agentId > 0, "Invalid agent ID");
        require(validatorId > 0, "Invalid validator ID");
        require(bytes(requestURI).length > 0, "Request URI cannot be empty");
        
        uint256 requestId = totalRequests++;
        
        validationRequests[requestId] = ValidationRequest({
            agentId: agentId,
            requester: msg.sender,
            validatorId: validatorId,
            requestURI: requestURI,
            requestHash: requestHash,
            timestamp: block.timestamp,
            completed: false
        });
        
        agentValidationRequests[agentId].push(requestId);
        validatorRequests[validatorId].push(requestId);
        
        emit ValidationRequested(
            requestId,
            agentId,
            validatorId,
            msg.sender,
            block.timestamp
        );
        
        return requestId;
    }
    
    /**
     * @dev Submit validation response
     * @param requestId Request ID being validated
     * @param score Validation score (0-100)
     * @param responseURI URI to validation response data
     * @param responseHash Hash of response data
     */
    function submitValidationResponse(
        uint256 requestId,
        uint8 score,
        string memory responseURI,
        bytes32 responseHash
    ) external {
        require(requestId < totalRequests, "Invalid request ID");
        require(score <= 100, "Score must be 0-100");
        require(!validationRequests[requestId].completed, "Request already completed");
        
        ValidationRequest storage request = validationRequests[requestId];
        
        validationResponses[requestId] = ValidationResponse({
            requestId: requestId,
            validatorId: request.validatorId,
            score: score,
            responseURI: responseURI,
            responseHash: responseHash,
            timestamp: block.timestamp
        });
        
        request.completed = true;
        
        emit ValidationResponseSubmitted(
            requestId,
            request.validatorId,
            score,
            block.timestamp
        );
    }
    
    /**
     * @dev Get validation request details
     * @param requestId Request ID
     * @return ValidationRequest struct
     */
    function getValidationRequest(uint256 requestId) external view returns (ValidationRequest memory) {
        require(requestId < totalRequests, "Invalid request ID");
        return validationRequests[requestId];
    }
    
    /**
     * @dev Get validation response details
     * @param requestId Request ID
     * @return ValidationResponse struct
     */
    function getValidationResponse(uint256 requestId) external view returns (ValidationResponse memory) {
        require(requestId < totalRequests, "Invalid request ID");
        require(validationRequests[requestId].completed, "Validation not completed");
        return validationResponses[requestId];
    }
    
    /**
     * @dev Get all validation requests for an agent
     * @param agentId Agent ID
     * @return Array of request IDs
     */
    function getAgentValidationRequests(uint256 agentId) external view returns (uint256[] memory) {
        return agentValidationRequests[agentId];
    }
    
    /**
     * @dev Get all validation requests assigned to a validator
     * @param validatorId Validator ID
     * @return Array of request IDs
     */
    function getValidatorRequests(uint256 validatorId) external view returns (uint256[] memory) {
        return validatorRequests[validatorId];
    }
    
    /**
     * @dev Check if validation request is completed
     * @param requestId Request ID
     * @return bool indicating completion status
     */
    function isValidationCompleted(uint256 requestId) external view returns (bool) {
        require(requestId < totalRequests, "Invalid request ID");
        return validationRequests[requestId].completed;
    }
    
    /**
     * @dev Get average validation score for an agent
     * @param agentId Agent ID
     * @return Average validation score (0-100), 0 if no validations
     */
    function getAverageValidationScore(uint256 agentId) external view returns (uint256) {
        uint256[] memory requests = agentValidationRequests[agentId];
        
        if (requests.length == 0) {
            return 0;
        }
        
        uint256 totalScore = 0;
        uint256 completedCount = 0;
        
        for (uint256 i = 0; i < requests.length; i++) {
            if (validationRequests[requests[i]].completed) {
                totalScore += validationResponses[requests[i]].score;
                completedCount++;
            }
        }
        
        if (completedCount == 0) {
            return 0;
        }
        
        return totalScore / completedCount;
    }
}

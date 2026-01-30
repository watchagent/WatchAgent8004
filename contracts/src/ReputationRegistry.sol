// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ReputationRegistry
 * @dev ERC-8004 Reputation Registry - Decentralized feedback system
 * @notice Manages reputation and feedback for AI agents
 */
contract ReputationRegistry {
    struct Feedback {
        uint256 agentId;
        address reviewer;
        uint8 score; // 0-100
        string[] tags;
        string dataURI; // IPFS link to full feedback
        bytes32 dataHash;
        uint256 timestamp;
    }
    
    struct FeedbackAuthorization {
        uint256 agentId;
        address client;
        bool authorized;
        uint256 authorizedAt;
    }
    
    // Agent ID => Feedback array
    mapping(uint256 => Feedback[]) public agentFeedback;
    
    // Agent ID => Client => Authorization
    mapping(uint256 => mapping(address => FeedbackAuthorization)) public feedbackAuthorizations;
    
    // Feedback counter
    uint256 public totalFeedbackCount;
    
    event FeedbackAuthorized(
        uint256 indexed agentId,
        address indexed client,
        uint256 timestamp
    );
    
    event FeedbackSubmitted(
        uint256 indexed agentId,
        address indexed reviewer,
        uint8 score,
        uint256 feedbackIndex,
        uint256 timestamp
    );
    
    event FeedbackRevoked(
        uint256 indexed agentId,
        address indexed client,
        uint256 timestamp
    );
    
    /**
     * @dev Authorize a client to submit feedback
     * @param agentId Agent ID to authorize feedback for
     * @param client Address authorized to submit feedback
     */
    function authorizeFeedback(uint256 agentId, address client) external {
        require(client != address(0), "Invalid client address");
        require(!feedbackAuthorizations[agentId][client].authorized, "Already authorized");
        
        feedbackAuthorizations[agentId][client] = FeedbackAuthorization({
            agentId: agentId,
            client: client,
            authorized: true,
            authorizedAt: block.timestamp
        });
        
        emit FeedbackAuthorized(agentId, client, block.timestamp);
    }
    
    /**
     * @dev Submit feedback for an agent
     * @param agentId Agent ID receiving feedback
     * @param score Score (0-100)
     * @param tags Feedback tags
     * @param dataURI URI to full feedback data
     * @param dataHash Hash of feedback data
     */
    function submitFeedback(
        uint256 agentId,
        uint8 score,
        string[] memory tags,
        string memory dataURI,
        bytes32 dataHash
    ) external {
        require(score <= 100, "Score must be 0-100");
        require(
            feedbackAuthorizations[agentId][msg.sender].authorized,
            "Not authorized to submit feedback"
        );
        
        Feedback memory feedback = Feedback({
            agentId: agentId,
            reviewer: msg.sender,
            score: score,
            tags: tags,
            dataURI: dataURI,
            dataHash: dataHash,
            timestamp: block.timestamp
        });
        
        agentFeedback[agentId].push(feedback);
        totalFeedbackCount++;
        
        uint256 feedbackIndex = agentFeedback[agentId].length - 1;
        
        emit FeedbackSubmitted(agentId, msg.sender, score, feedbackIndex, block.timestamp);
    }
    
    /**
     * @dev Revoke feedback authorization
     * @param agentId Agent ID
     * @param client Client to revoke
     */
    function revokeFeedbackAuthorization(uint256 agentId, address client) external {
        require(
            feedbackAuthorizations[agentId][client].authorized,
            "Not currently authorized"
        );
        
        feedbackAuthorizations[agentId][client].authorized = false;
        
        emit FeedbackRevoked(agentId, client, block.timestamp);
    }
    
    /**
     * @dev Get all feedback for an agent
     * @param agentId Agent ID
     * @return Array of feedback
     */
    function getAgentFeedback(uint256 agentId) external view returns (Feedback[] memory) {
        return agentFeedback[agentId];
    }
    
    /**
     * @dev Get feedback count for an agent
     * @param agentId Agent ID
     * @return Number of feedback entries
     */
    function getFeedbackCount(uint256 agentId) external view returns (uint256) {
        return agentFeedback[agentId].length;
    }
    
    /**
     * @dev Calculate average score for an agent
     * @param agentId Agent ID
     * @return Average score (0-100), 0 if no feedback
     */
    function getAverageScore(uint256 agentId) external view returns (uint256) {
        Feedback[] memory feedback = agentFeedback[agentId];
        
        if (feedback.length == 0) {
            return 0;
        }
        
        uint256 totalScore = 0;
        for (uint256 i = 0; i < feedback.length; i++) {
            totalScore += feedback[i].score;
        }
        
        return totalScore / feedback.length;
    }
    
    /**
     * @dev Check if client is authorized for feedback
     * @param agentId Agent ID
     * @param client Client address
     * @return bool indicating authorization status
     */
    function isAuthorized(uint256 agentId, address client) external view returns (bool) {
        return feedbackAuthorizations[agentId][client].authorized;
    }
    
    /**
     * @dev Get specific feedback entry
     * @param agentId Agent ID
     * @param index Feedback index
     * @return Feedback struct
     */
    function getFeedback(uint256 agentId, uint256 index) external view returns (Feedback memory) {
        require(index < agentFeedback[agentId].length, "Index out of bounds");
        return agentFeedback[agentId][index];
    }
}

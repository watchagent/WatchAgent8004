// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title IdentityRegistry
 * @dev ERC-8004 Identity Registry - ERC-721 based agent identity system
 * @notice Provides unique, portable identities for AI agents
 */
contract IdentityRegistry is ERC721URIStorage, Ownable {
    // Agent counter for unique IDs
    uint256 private _nextAgentId;
    
    // Mapping from agent ID to metadata
    mapping(uint256 => AgentMetadata) public agentMetadata;
    
    // Mapping from domain to agent ID
    mapping(string => uint256) public domainToAgentId;
    
    struct AgentMetadata {
        string name;
        string domain;
        address wallet;
        uint256 registeredAt;
        bool active;
    }
    
    event AgentRegistered(
        uint256 indexed agentId,
        address indexed owner,
        string name,
        string domain
    );
    
    event AgentUpdated(
        uint256 indexed agentId,
        string newTokenURI
    );
    
    event AgentDeactivated(uint256 indexed agentId);
    
    constructor() ERC721("ERC8004 Agent Identity", "AGENT") Ownable(msg.sender) {
        _nextAgentId = 1;
    }
    
    /**
     * @dev Register a new agent
     * @param name Agent name
     * @param domain Agent domain
     * @param tokenURI URI pointing to agent registration file
     * @return agentId The ID of the newly registered agent
     */
    function registerAgent(
        string memory name,
        string memory domain,
        string memory tokenURI
    ) external returns (uint256) {
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(domain).length > 0, "Domain cannot be empty");
        require(domainToAgentId[domain] == 0, "Domain already registered");
        
        uint256 agentId = _nextAgentId++;
        
        // Mint NFT to caller
        _safeMint(msg.sender, agentId);
        _setTokenURI(agentId, tokenURI);
        
        // Store metadata
        agentMetadata[agentId] = AgentMetadata({
            name: name,
            domain: domain,
            wallet: msg.sender,
            registeredAt: block.timestamp,
            active: true
        });
        
        domainToAgentId[domain] = agentId;
        
        emit AgentRegistered(agentId, msg.sender, name, domain);
        
        return agentId;
    }
    
    /**
     * @dev Update agent registration file URI
     * @param agentId Agent ID
     * @param newTokenURI New URI for registration file
     */
    function updateAgentURI(uint256 agentId, string memory newTokenURI) external {
        require(ownerOf(agentId) == msg.sender, "Not agent owner");
        require(agentMetadata[agentId].active, "Agent not active");
        
        _setTokenURI(agentId, newTokenURI);
        
        emit AgentUpdated(agentId, newTokenURI);
    }
    
    /**
     * @dev Deactivate an agent
     * @param agentId Agent ID to deactivate
     */
    function deactivateAgent(uint256 agentId) external {
        require(ownerOf(agentId) == msg.sender, "Not agent owner");
        require(agentMetadata[agentId].active, "Agent already inactive");
        
        agentMetadata[agentId].active = false;
        
        emit AgentDeactivated(agentId);
    }
    
    /**
     * @dev Get agent metadata
     * @param agentId Agent ID
     * @return Agent metadata struct
     */
    function getAgentMetadata(uint256 agentId) external view returns (AgentMetadata memory) {
        require(_ownerOf(agentId) != address(0), "Agent does not exist");
        return agentMetadata[agentId];
    }
    
    /**
     * @dev Check if an agent is active
     * @param agentId Agent ID
     * @return bool indicating if agent is active
     */
    function isAgentActive(uint256 agentId) external view returns (bool) {
        return agentMetadata[agentId].active;
    }
    
    /**
     * @dev Get agent ID by domain
     * @param domain Agent domain
     * @return Agent ID (0 if not found)
     */
    function getAgentByDomain(string memory domain) external view returns (uint256) {
        return domainToAgentId[domain];
    }
    
    /**
     * @dev Get total number of registered agents
     * @return Total agent count
     */
    function totalAgents() external view returns (uint256) {
        return _nextAgentId - 1;
    }
}

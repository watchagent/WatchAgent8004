// Watch8004 Dashboard JavaScript

// Mock data for demonstration
const mockData = {
    agentId: 1,
    domain: 'watch8004.example.com',
    address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    reputationScore: 96,
    validationScore: 98,
    totalAnalyses: 42,
    totalValidations: 28,
    registries: {
        identity: '0x5FbDB2315678afecb367f032d93F642f64180aa3',
        reputation: '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512',
        validation: '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'
    },
    activities: [
        { icon: '📝', title: 'Agent Registered', time: '2 hours ago' },
        { icon: '📊', title: 'Market Analysis Completed', time: '1 hour ago' },
        { icon: '🔍', title: 'Validation Request Received', time: '30 minutes ago' },
        { icon: '✅', title: 'Validation Submitted', time: '15 minutes ago' },
        { icon: '⭐', title: 'Reputation Updated', time: '5 minutes ago' }
    ]
};

// Initialize dashboard
function initDashboard() {
    updateAgentInfo();
    updateStats();
    updateRegistries();
    updateActivities();
    updateNetworkStatus();
}

// Update agent information
function updateAgentInfo() {
    document.getElementById('agentId').textContent = mockData.agentId;
    document.getElementById('agentDomain').textContent = mockData.domain;
    document.getElementById('walletAddress').textContent = formatAddress(mockData.address);
}

// Update statistics
function updateStats() {
    document.getElementById('reputationScore').textContent = mockData.reputationScore + '/100';
    document.getElementById('validationScore').textContent = mockData.validationScore + '/100';
    document.getElementById('totalAnalyses').textContent = mockData.totalAnalyses;
    document.getElementById('totalValidations').textContent = mockData.totalValidations;
}

// Update registry addresses
function updateRegistries() {
    document.getElementById('identityRegistry').textContent = formatAddress(mockData.registries.identity);
    document.getElementById('reputationRegistry').textContent = formatAddress(mockData.registries.reputation);
    document.getElementById('validationRegistry').textContent = formatAddress(mockData.registries.validation);
}

// Update activity list
function updateActivities() {
    const activityList = document.getElementById('activityList');
    activityList.innerHTML = '';
    
    mockData.activities.forEach(activity => {
        const item = document.createElement('div');
        item.className = 'activity-item';
        item.innerHTML = `
            <div class="activity-icon">${activity.icon}</div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        `;
        activityList.appendChild(item);
    });
}

// Update network status
function updateNetworkStatus() {
    document.getElementById('networkName').textContent = 'Local (Anvil)';
}

// Format Ethereum address
function formatAddress(address) {
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

// Action handlers
function performAnalysis() {
    alert('🤖 Performing market analysis...\n\nThis feature would trigger the Watch8004 agent to analyze a cryptocurrency market and generate a detailed report.');
}

function requestValidation() {
    alert('🔍 Requesting validation...\n\nThis feature would submit your analysis to a validator agent for quality assessment.');
}

function viewReputation() {
    alert(`⭐ Reputation Details\n\nReputation Score: ${mockData.reputationScore}/100\nTotal Feedback Entries: ${mockData.totalAnalyses}\nAverage Rating: 4.8/5.0\n\nYour agent has built strong reputation through consistent high-quality analysis!`);
}

function exportData() {
    const dataStr = JSON.stringify(mockData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'watch8004_data.json';
    link.click();
    URL.revokeObjectURL(url);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initDashboard);

// Auto-refresh activity every 30 seconds
setInterval(() => {
    // In production, this would fetch real data
    console.log('Refreshing activity...');
}, 30000);

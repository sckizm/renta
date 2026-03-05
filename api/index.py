# api/index.py
from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# External API configuration - change this to your actual API
EXTERNAL_API_URL = os.environ.get('EXTERNAL_API_URL', 'https://api.sckizm.shop')

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lord Sorgu Paneli</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
        }

        /* Header */
        .header {
            background: white;
            border-radius: 20px 20px 0 0;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .bot-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .bot-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }

        .bot-details h1 {
            font-size: 20px;
            color: #333;
            margin-bottom: 5px;
        }

        .bot-username {
            color: #667eea;
            font-size: 14px;
            text-decoration: none;
        }

        /* Token Section */
        .token-section {
            background: white;
            padding: 20px 25px;
            border-top: 1px solid #eee;
        }

        .token-label {
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .token-box {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 12px;
        }

        .token-text {
            flex: 1;
            font-family: monospace;
            font-size: 14px;
            color: #333;
            word-break: break-all;
        }

        .token-actions {
            display: flex;
            gap: 10px;
        }

        .btn-icon {
            background: none;
            border: none;
            color: #667eea;
            cursor: pointer;
            font-size: 14px;
            padding: 5px;
        }

        .btn-icon:hover {
            color: #764ba2;
        }

        .read-more {
            color: #667eea;
            text-decoration: none;
            font-size: 12px;
            margin-top: 8px;
            display: inline-block;
        }

        /* Settings Section */
        .settings-section {
            background: white;
            padding: 20px 25px;
            border-top: 1px solid #eee;
        }

        .section-title {
            color: #666;
            font-size: 13px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .settings-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .setting-item {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #333;
            cursor: pointer;
            padding: 10px;
            border-radius: 10px;
            transition: background 0.3s ease;
        }

        .setting-item:hover {
            background: #f0f2f5;
        }

        .setting-icon {
            width: 40px;
            height: 40px;
            background: #f0f2f5;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .setting-text {
            font-size: 14px;
            font-weight: 500;
        }

        /* Monetization Section */
        .monetization-section {
            background: white;
            padding: 20px 25px;
            border-top: 1px solid #eee;
        }

        .monetization-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 15px;
        }

        .monetization-item {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #333;
            cursor: pointer;
            padding: 10px;
            border-radius: 10px;
            transition: background 0.3s ease;
        }

        .monetization-item:hover {
            background: #f0f2f5;
        }

        .monetization-note {
            background: #f0f2f5;
            padding: 15px;
            border-radius: 10px;
            color: #666;
            font-size: 13px;
            line-height: 1.5;
            margin-top: 15px;
        }

        /* Query Panel */
        .query-panel {
            background: white;
            border-radius: 0 0 20px 20px;
            padding: 25px;
            border-top: 1px solid #eee;
        }

        .query-title {
            color: #666;
            font-size: 13px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .query-grid {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .query-button {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 15px;
            width: 100%;
        }

        .query-button:hover {
            background: #f0f2f5;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .query-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
        }

        .query-content {
            flex: 1;
        }

        .query-name {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }

        .query-desc {
            font-size: 13px;
            color: #666;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            padding: 20px;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 20px;
            width: 100%;
            max-width: 500px;
            max-height: 80vh;
            overflow-y: auto;
        }

        .modal-header {
            padding: 20px;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            background: white;
            z-index: 10;
        }

        .modal-header h2 {
            font-size: 18px;
            color: #333;
        }

        .modal-close {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #999;
            padding: 5px 10px;
        }

        .modal-close:hover {
            color: #333;
        }

        .modal-body {
            padding: 20px;
        }

        .modal-footer {
            padding: 20px;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            position: sticky;
            bottom: 0;
            background: white;
        }

        .input-field {
            width: 100%;
            padding: 12px;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            font-size: 14px;
            margin-bottom: 15px;
            font-family: inherit;
        }

        .input-field:focus {
            outline: none;
            border-color: #667eea;
        }

        select.input-field {
            appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 12px center;
            background-size: 16px;
        }

        textarea.input-field {
            min-height: 100px;
            resize: vertical;
        }

        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-secondary {
            background: #f0f2f5;
            color: #333;
        }

        .btn-secondary:hover {
            background: #e4e6e9;
        }

        .result-area {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            margin-top: 15px;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading.active {
            display: block;
        }

        .loading-spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error-message {
            color: #dc3545;
            font-size: 14px;
            margin-top: 10px;
            padding: 10px;
            background: #fff5f5;
            border-radius: 8px;
            border-left: 3px solid #dc3545;
        }

        .success-message {
            color: #28a745;
            font-size: 14px;
            margin-top: 10px;
            padding: 10px;
            background: #f0fff4;
            border-radius: 8px;
            border-left: 3px solid #28a745;
        }

        /* Telegram Web App support */
        .telegram-button {
            background: var(--tg-theme-button-color, #667eea);
            color: var(--tg-theme-button-text-color, white);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="bot-info">
                <div class="bot-avatar">🤖</div>
                <div class="bot-details">
                    <h1>Lord Sorgu Paneli</h1>
                    <a href="#" class="bot-username" id="botUsername">@LordSorguBot</a>
                </div>
            </div>
        </div>

        <!-- Token Section -->
        <div class="token-section">
            <div class="token-label">API Token</div>
            <div class="token-box">
                <span class="token-text" id="apiToken">••••••••••••••••</span>
                <div class="token-actions">
                    <button class="btn-icon" onclick="copyToken()" title="Copy token">📋</button>
                    <button class="btn-icon" onclick="revokeToken()" title="Revoke token">🔄</button>
                </div>
            </div>
            <a href="#" class="read-more" onclick="showReadMore()">Read more ></a>
        </div>

        <!-- Settings Section -->
        <div class="settings-section">
            <div class="section-title">Settings</div>
            <div class="settings-grid">
                <div class="setting-item" onclick="showSetting('edit')">
                    <span class="setting-icon">✏️</span>
                    <span class="setting-text">Edit Info</span>
                </div>
                <div class="setting-item" onclick="showSetting('commands')">
                    <span class="setting-icon">📝</span>
                    <span class="setting-text">Commands</span>
                </div>
                <div class="setting-item" onclick="showSetting('miniapps')">
                    <span class="setting-icon">📱</span>
                    <span class="setting-text">Mini Apps</span>
                </div>
                <div class="setting-item" onclick="showSetting('botsettings')">
                    <span class="setting-icon">⚙️</span>
                    <span class="setting-text">Bot Settings</span>
                </div>
                <div class="setting-item" onclick="showSetting('games')">
                    <span class="setting-icon">🎮</span>
                    <span class="setting-text">Games</span>
                </div>
            </div>
        </div>

        <!-- Monetization Section -->
        <div class="monetization-section">
            <div class="section-title">Monetization</div>
            <div class="monetization-grid">
                <div class="monetization-item" onclick="showMonetization('payments')">
                    <span class="setting-icon">💰</span>
                    <span class="setting-text">Payments</span>
                </div>
                <div class="monetization-item" onclick="showMonetization('stars')">
                    <span class="setting-icon">⭐</span>
                    <span class="setting-text">Telegram Stars</span>
                </div>
            </div>
            <div class="monetization-note">
                Telegram Stars are designed for digital content and in-app items. If you want to sell physical goods, use Payments
            </div>
        </div>

        <!-- Query Panel -->
        <div class="query-panel">
            <div class="query-title">Query Types</div>
            <div class="query-grid">
                <button class="query-button" onclick="openQueryModal('user')">
                    <div class="query-icon">👤</div>
                    <div class="query-content">
                        <div class="query-name">User Info Query</div>
                        <div class="query-desc">Get detailed user information from API</div>
                    </div>
                </button>

                <button class="query-button" onclick="openQueryModal('posts')">
                    <div class="query-icon">📄</div>
                    <div class="query-content">
                        <div class="query-name">Posts Query</div>
                        <div class="query-desc">Fetch and analyze posts from API</div>
                    </div>
                </button>

                <button class="query-button" onclick="openQueryModal('comments')">
                    <div class="query-icon">💬</div>
                    <div class="query-content">
                        <div class="query-name">Comments Query</div>
                        <div class="query-desc">Retrieve and filter comments</div>
                    </div>
                </button>

                <button class="query-button" onclick="openQueryModal('todos')">
                    <div class="query-icon">✅</div>
                    <div class="query-content">
                        <div class="query-name">Todos Query</div>
                        <div class="query-desc">Check and manage todo items</div>
                    </div>
                </button>

                <button class="query-button" onclick="openQueryModal('custom')">
                    <div class="query-icon">🔧</div>
                    <div class="query-content">
                        <div class="query-name">Custom Query</div>
                        <div class="query-desc">Send custom API request</div>
                    </div>
                </button>
            </div>
        </div>
    </div>

    <!-- Query Modal -->
    <div class="modal" id="queryModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Query</h2>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div id="queryInputs">
                    <!-- Dynamic inputs will be inserted here -->
                </div>
                <div class="loading" id="loading">
                    <div class="loading-spinner"></div>
                    <div>Processing query...</div>
                </div>
                <div class="result-area" id="result"></div>
                <div class="error-message" id="error"></div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal()">Close</button>
                <button class="btn btn-primary" onclick="executeQuery()" id="executeBtn">Execute Query</button>
            </div>
        </div>
    </div>

    <script>
        // Initialize Telegram Web App
        let tg = null;
        let currentQueryType = '';
        let apiToken = 'demo-token-' + Math.random().toString(36).substr(2, 9);

        // Try to initialize Telegram Web App
        try {
            if (window.Telegram && window.Telegram.WebApp) {
                tg = window.Telegram.WebApp;
                tg.ready();
                tg.expand(); // Expand to full height
                
                // Set theme colors if available
                if (tg.themeParams) {
                    document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
                    document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
                    document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#667eea');
                    document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
                }
            }
        } catch (e) {
            console.log('Not running in Telegram');
        }

        function copyToken() {
            navigator.clipboard.writeText(apiToken).then(() => {
                showNotification('Token copied to clipboard!', 'success');
            }).catch(() => {
                alert('Token: ' + apiToken);
            });
        }

        function revokeToken() {
            if(confirm('Are you sure you want to revoke the token?')) {
                apiToken = 'new-token-' + Math.random().toString(36).substr(2, 9);
                document.getElementById('apiToken').textContent = '••••••••••••••••';
                showNotification('Token revoked successfully!', 'success');
            }
        }

        function showReadMore() {
            alert('API tokens are used to authenticate requests to your bot. Keep them secure!');
        }

        function showSetting(type) {
            const messages = {
                'edit': 'Edit bot information',
                'commands': 'Manage bot commands',
                'miniapps': 'Configure mini apps',
                'botsettings': 'Bot settings panel',
                'games': 'Game management'
            };
            showNotification(messages[type] || type, 'info');
        }

        function showMonetization(type) {
            const messages = {
                'payments': 'Payment configuration',
                'stars': 'Telegram Stars settings'
            };
            showNotification(messages[type] || type, 'info');
        }

        function showNotification(message, type) {
            const errorEl = document.getElementById('error');
            if (type === 'error') {
                errorEl.innerHTML = message;
                errorEl.className = 'error-message';
                setTimeout(() => errorEl.innerHTML = '', 3000);
            } else {
                // Create temporary notification
                const notif = document.createElement('div');
                notif.className = 'success-message';
                notif.textContent = message;
                notif.style.position = 'fixed';
                notif.style.bottom = '20px';
                notif.style.left = '20px';
                notif.style.right = '20px';
                notif.style.zIndex = '2000';
                document.body.appendChild(notif);
                setTimeout(() => notif.remove(), 3000);
            }
        }

        function openQueryModal(type) {
            currentQueryType = type;
            const modal = document.getElementById('queryModal');
            const title = document.getElementById('modalTitle');
            const inputs = document.getElementById('queryInputs');
            
            // Clear previous inputs
            inputs.innerHTML = '';
            
            switch(type) {
                case 'user':
                    title.textContent = 'User Info Query';
                    inputs.innerHTML = `
                        <input type="number" id="userId" class="input-field" placeholder="Enter User ID (1-10)" min="1" max="10" value="1">
                    `;
                    break;
                case 'posts':
                    title.textContent = 'Posts Query';
                    inputs.innerHTML = `
                        <input type="number" id="userId" class="input-field" placeholder="Filter by User ID (optional)" min="1" max="10">
                    `;
                    break;
                case 'comments':
                    title.textContent = 'Comments Query';
                    inputs.innerHTML = `
                        <input type="number" id="postId" class="input-field" placeholder="Filter by Post ID (optional)" min="1" max="100">
                    `;
                    break;
                case 'todos':
                    title.textContent = 'Todos Query';
                    inputs.innerHTML = `
                        <select id="completed" class="input-field">
                            <option value="">All Todos</option>
                            <option value="true">Completed</option>
                            <option value="false">Not Completed</option>
                        </select>
                    `;
                    break;
                case 'custom':
                    title.textContent = 'Custom Query';
                    inputs.innerHTML = `
                        <input type="text" id="endpoint" class="input-field" placeholder="Endpoint (e.g., /posts/1)" value="/posts/1">
                        <select id="method" class="input-field">
                            <option value="GET">GET</option>
                            <option value="POST">POST</option>
                            <option value="PUT">PUT</option>
                            <option value="DELETE">DELETE</option>
                        </select>
                        <textarea id="body" class="input-field" placeholder="Request Body (JSON)"></textarea>
                    `;
                    break;
            }
            
            // Reset result and error
            document.getElementById('result').innerHTML = '';
            document.getElementById('error').innerHTML = '';
            document.getElementById('loading').classList.remove('active');
            
            // Show modal
            modal.classList.add('active');
            
            // If in Telegram, configure main button
            if (tg) {
                tg.MainButton.setText('Execute Query');
                tg.MainButton.show();
                tg.MainButton.onClick(executeQuery);
            }
        }

        function closeModal() {
            document.getElementById('queryModal').classList.remove('active');
            document.getElementById('loading').classList.remove('active');
            
            // Hide Telegram main button if exists
            if (tg) {
                tg.MainButton.hide();
            }
        }

        async function executeQuery() {
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            const executeBtn = document.getElementById('executeBtn');
            
            loading.classList.add('active');
            result.innerHTML = '';
            error.innerHTML = '';
            executeBtn.disabled = true;
            
            try {
                let response;
                let url = '';
                
                switch(currentQueryType) {
                    case 'user':
                        const userId = document.getElementById('userId').value;
                        url = `/api/query/user?userId=${userId}`;
                        response = await fetch(url);
                        break;
                    case 'posts':
                        const userFilter = document.getElementById('userId').value;
                        url = `/api/query/posts${userFilter ? `?userId=${userFilter}` : ''}`;
                        response = await fetch(url);
                        break;
                    case 'comments':
                        const postFilter = document.getElementById('postId').value;
                        url = `/api/query/comments${postFilter ? `?postId=${postFilter}` : ''}`;
                        response = await fetch(url);
                        break;
                    case 'todos':
                        const completed = document.getElementById('completed').value;
                        url = `/api/query/todos${completed ? `?completed=${completed}` : ''}`;
                        response = await fetch(url);
                        break;
                    case 'custom':
                        const endpoint = document.getElementById('endpoint').value;
                        const method = document.getElementById('method').value;
                        const body = document.getElementById('body').value;
                        
                        const requestBody = {
                            endpoint: endpoint,
                            method: method
                        };
                        
                        if (body) {
                            try {
                                requestBody.body = JSON.parse(body);
                            } catch (e) {
                                throw new Error('Invalid JSON in request body');
                            }
                        }
                        
                        response = await fetch('/api/query/custom', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(requestBody)
                        });
                        break;
                }
                
                const data = await response.json();
                
                if(response.ok) {
                    result.innerHTML = JSON.stringify(data, null, 2);
                    // Send data to Telegram if in WebApp
                    if (tg) {
                        tg.sendData(JSON.stringify(data));
                    }
                } else {
                    error.innerHTML = data.error || 'An error occurred';
                }
            } catch(err) {
                error.innerHTML = 'Error executing query: ' + err.message;
            } finally {
                loading.classList.remove('active');
                executeBtn.disabled = false;
            }
        }

        // Close modal when clicking outside
        document.getElementById('queryModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // Handle ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """Serve the main web app page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/query/user')
def query_user():
    """Query user information from external API"""
    try:
        user_id = request.args.get('userId', 1)
        response = requests.get(f"{EXTERNAL_API_URL}/users/{user_id}", timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "User not found"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query/posts')
def query_posts():
    """Query posts from external API"""
    try:
        user_id = request.args.get('userId')
        url = f"{EXTERNAL_API_URL}/posts"
        if user_id:
            url += f"?userId={user_id}"
        
        response = requests.get(url, timeout=10)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query/comments')
def query_comments():
    """Query comments from external API"""
    try:
        post_id = request.args.get('postId')
        url = f"{EXTERNAL_API_URL}/comments"
        if post_id:
            url += f"?postId={post_id}"
        
        response = requests.get(url, timeout=10)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query/todos')
def query_todos():
    """Query todos from external API"""
    try:
        completed = request.args.get('completed')
        url = f"{EXTERNAL_API_URL}/todos"
        if completed:
            url += f"?completed={completed}"
        
        response = requests.get(url, timeout=10)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query/custom', methods=['POST'])
def query_custom():
    """Execute custom API request"""
    try:
        data = request.json
        endpoint = data.get('endpoint', '')
        method = data.get('method', 'GET')
        body = data.get('body')
        
        url = f"{EXTERNAL_API_URL}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=body, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=body, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return jsonify({"error": "Invalid method"}), 400
        
        try:
            return jsonify(response.json())
        except:
            return jsonify({"text": response.text})
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For local development
if __name__ == '__main__':
    print("=" * 50)
    print("Telegram Web App Starting...")
    print("=" * 50)
    print("\nConfiguration:")
    print(f"External API: {EXTERNAL_API_URL}")
    print("\nLocal URL: http://localhost:5000")
    print("\nFor Vercel deployment:")
    print("1. Push this code to GitHub")
    print("2. Import to Vercel")
    print("3. Set EXTERNAL_API_URL environment variable")
    print("\n" + "=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

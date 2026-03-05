# telegram_webapp_ui.py
from flask import Flask, render_template_string

app = Flask(__name__)

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
            background: #f0f2f5;
            min-height: 100vh;
            padding: 0;
            margin: 0;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }

        /* Header */
        .header {
            background: white;
            padding: 20px 16px;
            border-bottom: 1px solid #e9ecef;
        }

        .bot-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .bot-avatar {
            width: 54px;
            height: 54px;
            background: linear-gradient(135deg, #2AABEE 0%, #229ED9 100%);
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
            color: #000;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .bot-username {
            color: #2AABEE;
            font-size: 15px;
            text-decoration: none;
            font-weight: 500;
        }

        /* Settings Section */
        .settings-section {
            background: white;
            padding: 20px 16px;
            border-bottom: 1px solid #e9ecef;
        }

        .section-title {
            color: #8e8e93;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }

        .settings-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }

        .setting-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }

        .setting-icon {
            width: 48px;
            height: 48px;
            background: #f0f2f5;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .setting-text {
            font-size: 13px;
            font-weight: 500;
            color: #1c1c1e;
            text-align: center;
        }

        /* Monetization Section */
        .monetization-section {
            background: white;
            padding: 20px 16px;
            border-bottom: 1px solid #e9ecef;
        }

        .monetization-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 16px;
        }

        .monetization-item {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            padding: 8px;
            border-radius: 12px;
        }

        .monetization-icon {
            width: 40px;
            height: 40px;
            background: #f0f2f5;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .monetization-text {
            font-size: 15px;
            font-weight: 500;
            color: #1c1c1e;
        }

        .monetization-note {
            background: #f0f2f5;
            padding: 14px 16px;
            border-radius: 12px;
            color: #666;
            font-size: 13px;
            line-height: 1.5;
            margin-top: 8px;
        }

        /* Query Section */
        .query-section {
            background: white;
            padding: 20px 16px;
        }

        .query-title {
            color: #8e8e93;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }

        .query-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .query-item {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 12px 16px;
            background: #f8f9fa;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.2s ease;
            border: 1px solid #e9ecef;
        }

        .query-item:hover {
            background: #f0f2f5;
        }

        .query-icon {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #2AABEE 0%, #229ED9 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 22px;
            flex-shrink: 0;
        }

        .query-content {
            flex: 1;
        }

        .query-name {
            font-size: 16px;
            font-weight: 600;
            color: #1c1c1e;
            margin-bottom: 4px;
        }

        .query-desc {
            font-size: 13px;
            color: #8e8e93;
        }

        /* Separator */
        .separator {
            height: 8px;
            background: #f0f2f5;
            width: 100%;
        }

        /* For Telegram Web App */
        .telegram-button {
            background: var(--tg-theme-button-color, #2AABEE);
            color: var(--tg-theme-button-text-color, white);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="bot-info">
                <div class="bot-avatar">🔍</div>
                <div class="bot-details">
                    <h1>Lord Sorgu Paneli</h1>
                    <div class="bot-username">@LordSorguBot</div>
                </div>
            </div>
        </div>

        <!-- Settings Section -->
        <div class="settings-section">
            <div class="section-title">Settings</div>
            <div class="settings-grid">
                <div class="setting-item" onclick="alert('Edit Info')">
                    <span class="setting-icon">✏️</span>
                    <span class="setting-text">Edit Info</span>
                </div>
                <div class="setting-item" onclick="alert('Commands')">
                    <span class="setting-icon">📋</span>
                    <span class="setting-text">Commands</span>
                </div>
                <div class="setting-item" onclick="alert('Mini Apps')">
                    <span class="setting-icon">📱</span>
                    <span class="setting-text">Mini Apps</span>
                </div>
                <div class="setting-item" onclick="alert('Bot Settings')">
                    <span class="setting-icon">⚙️</span>
                    <span class="setting-text">Bot Settings</span>
                </div>
                <div class="setting-item" onclick="alert('Games')">
                    <span class="setting-icon">🎮</span>
                    <span class="setting-text">Games</span>
                </div>
                <div class="setting-item" style="visibility: hidden;"></div>
            </div>
        </div>

        <!-- Monetization Section -->
        <div class="monetization-section">
            <div class="section-title">Monetization</div>
            <div class="monetization-grid">
                <div class="monetization-item" onclick="alert('Payments')">
                    <span class="monetization-icon">💰</span>
                    <span class="monetization-text">Payments</span>
                </div>
                <div class="monetization-item" onclick="alert('Telegram Stars')">
                    <span class="monetization-icon">⭐</span>
                    <span class="monetization-text">Telegram Stars</span>
                </div>
            </div>
            <div class="monetization-note">
                Telegram Stars are designed for digital content and in-app items. If you want to sell physical goods, use Payments
            </div>
        </div>

        <!-- Separator -->
        <div class="separator"></div>

        <!-- Query Section -->
        <div class="query-section">
            <div class="query-title">Query Types</div>
            <div class="query-list">
                <div class="query-item" onclick="alert('User Info Query selected')">
                    <div class="query-icon">👤</div>
                    <div class="query-content">
                        <div class="query-name">User Info Query</div>
                        <div class="query-desc">Get detailed user information</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Posts Query selected')">
                    <div class="query-icon">📄</div>
                    <div class="query-content">
                        <div class="query-name">Posts Query</div>
                        <div class="query-desc">Fetch and analyze posts</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Comments Query selected')">
                    <div class="query-icon">💬</div>
                    <div class="query-content">
                        <div class="query-name">Comments Query</div>
                        <div class="query-desc">Retrieve and filter comments</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Todos Query selected')">
                    <div class="query-icon">✅</div>
                    <div class="query-content">
                        <div class="query-name">Todos Query</div>
                        <div class="query-desc">Check and manage todo items</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Custom Query selected')">
                    <div class="query-icon">🔧</div>
                    <div class="query-content">
                        <div class="query-name">Custom Query</div>
                        <div class="query-desc">Send custom API request</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Analytics Query selected')">
                    <div class="query-icon">📊</div>
                    <div class="query-content">
                        <div class="query-name">Analytics Query</div>
                        <div class="query-desc">Get analytics and statistics</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Search Query selected')">
                    <div class="query-icon">🔍</div>
                    <div class="query-content">
                        <div class="query-name">Search Query</div>
                        <div class="query-desc">Search through content</div>
                    </div>
                </div>

                <div class="query-item" onclick="alert('Filter Query selected')">
                    <div class="query-icon">⚡</div>
                    <div class="query-content">
                        <div class="query-name">Filter Query</div>
                        <div class="query-desc">Apply filters to data</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Telegram Web App if available
        try {
            if (window.Telegram && window.Telegram.WebApp) {
                const tg = window.Telegram.WebApp;
                tg.ready();
                tg.expand();
            }
        } catch (e) {
            console.log('Not running in Telegram');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("=" * 50)
    print("Telegram Web App UI")
    print("=" * 50)
    print("\nLocal URL: http://localhost:5000")
    print("\n" + "=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

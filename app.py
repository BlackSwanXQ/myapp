from flask import Flask, jsonify, render_template_string
from redis import Redis
import socket
import os

app = Flask(__name__)
redis = Redis(host='redis-service', port=6379, decode_responses=True)

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyApp | K3s Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .card {
            background: rgba(255,255,255,0.95);
            border-radius: 30px;
            padding: 50px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
            text-align: center;
            max-width: 600px;
            width: 90%;
            backdrop-filter: blur(10px);
        }
        h1 { color: #2a5298; font-size: 2.8em; margin-bottom: 20px; }
        .badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 50px;
            font-size: 0.4em;
        }
        .pod-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 20px;
            margin: 30px 0;
        }
        .pod-name {
            background: white;
            padding: 15px;
            border-radius: 15px;
            font-family: monospace;
            font-size: 1.1em;
            color: #2a5298;
            font-weight: bold;
        }
        .counter {
            font-size: 2.5em;
            font-weight: bold;
            color: #764ba2;
            margin: 20px 0;
        }
        .status {
            display: inline-block;
            background: #4caf50;
            color: white;
            padding: 5px 15px;
            border-radius: 50px;
            font-size: 0.8em;
        }
        .info-grid {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .info-item {
            background: rgba(42,82,152,0.1);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.8em;
        }
        button {
            background: #2a5298;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 50px;
            font-size: 1em;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s;
        }
        button:hover {
            background: #1e3c72;
            transform: scale(1.05);
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.75em;
            color: #888;
        }
        .git-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #24292e;
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 0.8em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="card">

        <h1>🚀 MyApp <span class="badge">v5.0</span></h1>
        <p>Running on Kubernetes K3s cluster with Redis</p>

        <div class="pod-card">
            <div style="margin-bottom: 10px;">📍 CURRENT POD</div>
            <div class="pod-name" id="pod-name">Loading...</div>
        </div>

        <div class="counter" id="counter">Loading...</div>

        <div class="status">✅ Cluster Status: Healthy</div>

        <div class="info-grid">
            <div class="info-item">🔄 Auto Deploy</div>
            <div class="info-item">📦 Harbor Registry</div>
            <div class="info-item">🔒 HTTPS</div>
            <div class="info-item">💾 Redis Storage</div>
        </div>

        <button onclick="location.reload()">🔄 Refresh Page</button>

        <a href="https://github.com/BlackSwanXQ/myapp" target="_blank" class="git-badge">
            📁 View on GitHub
        </a>

        <div class="footer">
            Powered by K3s • Redis • Ingress-Nginx • cert-manager
            <br>
            <span id="timestamp"></span>
        </div>
    </div>

    <script>
        function updateTimestamp() {
            document.getElementById('timestamp').innerText = '🕐 ' + new Date().toLocaleString();
        }

        function fetchData() {
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('counter').innerText = '👁️ Visits: ' + data.visits;
                    document.getElementById('pod-name').innerText = data.pod;
                })
                .catch(() => {
                    document.getElementById('counter').innerText = '❌ Redis connection error';
                });
        }

        fetchData();
        updateTimestamp();
        setInterval(updateTimestamp, 1000);
        setInterval(fetchData, 3000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/stats')
def stats():
    visits = redis.incr('visits')
    return jsonify({
        'visits': visits,
        'pod': socket.gethostname()
    })

@app.route('/health')
def health():
    try:
        redis.ping()
        return jsonify({'status': 'healthy', 'redis': 'connected'})
    except:
        return jsonify({'status': 'unhealthy', 'redis': 'disconnected'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

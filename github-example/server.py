from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
from datetime import datetime

def home(request):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hostname = os.environ.get('HOSTNAME', 'unknown')
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDEM - App Runner Demo</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            text-align: center;
        }}
        h1 {{ color: #667eea; font-size: 3em; margin-bottom: 20px; }}
        .emoji {{ font-size: 5em; margin: 20px 0; }}
        .info {{
            background: #f7f7f7;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .info-item {{ margin: 10px 0; font-size: 1.1em; }}
        .label {{ font-weight: bold; color: #667eea; }}
        .value {{ color: #555; font-family: 'Courier New', monospace; }}
        .badge {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 20px;
            font-weight: bold;
        }}
        .source {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>¡Hola EDEM! 👋</h1>
        <div class="emoji">🚀</div>
        <p style="font-size: 1.3em; color: #666; margin: 20px 0;">
            Tu aplicación está corriendo en <strong>AWS App Runner</strong>
        </p>
        <div class="info">
            <div class="info-item">
                <span class="label">🕐 Timestamp:</span><br>
                <span class="value">{timestamp}</span>
            </div>
            <div class="info-item">
                <span class="label">🖥️ Container:</span><br>
                <span class="value">{hostname}</span>
            </div>
        </div>
        <div class="badge">✅ Deployment Successful</div><br>
        <div class="source">📦 Source: GitHub</div>
    </div>
</body>
</html>"""
    return Response(html, content_type='text/html')

def health(request):
    return Response('{"status": "healthy"}', content_type='application/json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('health', '/health')
        config.add_view(home, route_name='home')
        config.add_view(health, route_name='health')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()

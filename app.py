from flask import Flask, render_template
import os
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def home():
    # Simular procesamiento para pruebas de carga
    time.sleep(2)
    return render_template('index.html', 
                         timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         hostname=os.environ.get('HOSTNAME', 'unknown'))

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

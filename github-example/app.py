from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from App Runner!'

@app.route('/health')
def health():
    return {'status': 'healthy'}

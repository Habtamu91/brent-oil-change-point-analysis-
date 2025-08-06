from flask import Flask, jsonify, render_template, send_from_directory
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__, static_folder='dashboard/frontend/build/static', template_folder='dashboard/frontend/build')

# ... (keep all your existing routes)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.template_folder, path)):
        return send_from_directory(app.template_folder, path)
    else:
        return send_from_directory(app.template_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
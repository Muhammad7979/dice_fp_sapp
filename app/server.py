# server.py
from flask import Flask, jsonify, render_template_string
import os
import hashlib
import random
import string

app = Flask(__name__)

DATA_DIR = "/serverdata"
FILE_PATH = f"{DATA_DIR}/data.txt"
os.makedirs(DATA_DIR, exist_ok=True)

def generate_data():
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
    checksum = hashlib.sha256(data.encode()).hexdigest()
    with open(FILE_PATH, "w") as f:
        f.write(data)
    return data, checksum

# HTML template for home page
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Server App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; margin-top: 20px; }
        #output {
            margin-top: 20px;
            display: none; /* hidden by default */
            white-space: pre-wrap; /* wrap long text */
            word-break: break-word; /* wrap very long tokens */
            background: #f2f2f2;
            padding: 20px;
            border-radius: 8px;
            max-width: 90%; /* fit screen width */
            margin-left: auto;
            margin-right: auto;
            text-align: left;
        }
        h1 { margin-bottom: 10px; }
        p { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Server App</h1>
    <p>Click the button below to generate random data and its checksum:</p>
    <button onclick="fetchData()">Generate Data</button>
    <div id="output"></div>

    <script>
        function fetchData() {
            fetch('/data')
                .then(response => response.json())
                .then(result => {
                    const box = document.getElementById('output');
                    box.style.display = 'block'; // show box on button click
                    box.textContent =
                        'Data:\\n' + result.data + '\\n\\nChecksum:\\n' + result.checksum;
                })
                .catch(err => {
                    const box = document.getElementById('output');
                    box.style.display = 'block';
                    box.textContent = 'Error fetching data';
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/data")
def get_data():
    data, checksum = generate_data()
    return jsonify({
        "data": data,
        "checksum": checksum
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
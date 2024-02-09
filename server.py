import os
import subprocess
from flask import Flask, send_from_directory

try:
    # Attempt to import Flask components
    from flask import Flask, send_from_directory
except ImportError:
    print("Flask is not installed. Please run `$ pip3 install flask` and try again.")
    exit(1)

# Define the directory for serving static files
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')
app = Flask(__name__)
# Disable caching for all static files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET'])
def serve_directory_index():
    if os.path.exists("app.py"):
        # If app.py exists, execute and return its output
        process = subprocess.Popen(['python3', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, _ = process.communicate()
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return f"<pre style='color: red;'>{stdout.decode('utf-8')}</pre>"
    elif os.path.exists("index.html"):
        # Serve index.html if it exists
        return send_from_directory(static_file_dir, 'index.html')
    else:
        # Return a 404 error page if index.html is missing
        return ("<h1 align='center'>404 Not Found</h1>"
                "<h2 align='center'>Missing index.html file.</h2>"
                "<p align='center'><img src='https://github.com/4GeeksAcademy/html-hello/blob/main/.vscode/rigo-baby.jpeg?raw=true' /></p>"), 404

@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
    # Adjust path if the requested file does not exist
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')
    response = send_from_directory(static_file_dir, path)
    # Set cache control header to avoid caching
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

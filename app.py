from flask import Flask, render_template, send_from_directory, abort, request, redirect, Response
from werkzeug.utils import secure_filename
import hashlib
import os

from config import log_paths

app = Flask(__name__)

password = os.getenv('LOGS_VIEWER_PASSWORD', 'ABCDE')
r_url = os.getenv('LOGS_VIEWER_REDIRECT', 'https://edm115.dev')
port = int(os.getenv('LOGS_VIEWER_PORT', 10000))
hashed_password = hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html', hashed_password=hashed_password, redirect_url=r_url)

@app.route('/admin')
def admin():
    log_files = {}
    client_pass = request.args.get('passwd', '')
    if client_pass == password:
        for bot, path in log_paths.items():
            if os.path.exists(path):
                files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))].sort()
                log_files[bot] = files
        return render_template('admin.html', log_files=log_files, hashed_password=hashed_password)
    else:
        return redirect(r_url)

@app.route('/logs/<bot>/<filename>')
def log_file(bot, filename):
    dl = request.args.get('dl', '')
    if bot in log_paths and os.path.exists(log_paths[bot]):
        secure_path = os.path.join(log_paths[bot], secure_filename(filename))
        try:
            if dl == '1':
                return send_from_directory(log_paths[bot], filename, as_attachment=False)
            else:
                with open(secure_path, 'r') as f:
                    content = f.read()
                return Response(content, mimetype='text/plain')
        except FileNotFoundError:
            abort(404)
    else:
        return redirect(r_url)

if __name__ == '__main__':
    app.run(debug=False, port=port)

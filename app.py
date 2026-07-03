from flask import Flask, render_template, jsonify
from ping_utils import check_devices

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") # fetches the template from the html file

@app.route("/api/status")
def status():
    return jsonify(check_devices())

if __name__ == '__main__':
    app.run(debug=False)
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Simpan nilai rata-rata suhu saat ini (nilai awalnya bisa 0)
current_average_temperature = 0

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/update_average_temperature', methods=['POST'])
# def update_average_temperature():
#     global current_average_temperature
#     data = request.get_json()
#     current_average_temperature = data['average_temperature']
#     return 'OK'

# @app.route('/average_temperature')
# def get_average_temperature():
#     return str(current_average_temperature)

if __name__ == '__main__':
    app.run(debug=True)

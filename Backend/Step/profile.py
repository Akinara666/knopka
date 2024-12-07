from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_profile', methods=['POST'])
def get_profile():
    # Здесь можно добавить логику для получения данных профиля из базы данных или другого источника
    profile_data = {
        'name': 'Макс',
        'email': 'maximmaximovich3822@mail.com',
        'registration_date': '23.11.2024'
    }
    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(debug=True)
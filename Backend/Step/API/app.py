from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример эндпоинта для получения данных
@app.route('/get-data', methods=['GET'])
def get_data():
    data = {"message": "Привет! Это тестовый GET запрос."}
    return jsonify(data)

# Пример эндпоинта для отправки данных
@app.route('/post-data', methods=['POST'])
def post_data():
    content = request.json  # Получаем JSON данные из запроса
    response = {"received_data": content}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

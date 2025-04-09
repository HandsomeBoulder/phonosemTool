from flask import Flask, jsonify, request
from flask_cors import CORS  # Позволяет фронту делать запросы к API
from phonosemModule import phonosemTool

app = Flask(__name__)
CORS(app)  # Разрешаем CORS

@app.route('/api/data', methods=['POST'])
def data():
    data = request.json  # Получаем JSON-данные
    input_string = data.get('text')  # Извлекаем поле "text"
    items = phonosemTool(input_string)
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Запуск на порту 5000
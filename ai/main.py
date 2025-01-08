from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from model import Regression_Algorithm
from utils import read_data, preprocess_data
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load và chuẩn bị dữ liệu
data_path = "data/students_dataset.xlsx"
raw_data = read_data(data_path)
data = preprocess_data(raw_data)

# Mã hóa dữ liệu
le_gender = LabelEncoder()
le_economy = LabelEncoder()
le_health = LabelEncoder()

data['Giới tính'] = le_gender.fit_transform(data['Giới tính'])
data['Tình hình kinh tế'] = le_economy.fit_transform(data['Tình hình kinh tế'])
data['Tình hình sức khỏe'] = le_health.fit_transform(data['Tình hình sức khỏe'])

X = data[['Tình hình kinh tế', 'GPA', 'Số ngày vắng (Không phép)', 'Làm thêm', 'Tình hình sức khỏe']].values
y = data['Kết quả'].values

# Tách dữ liệu và huấn luyện mô hình
split_index = int(0.8 * len(X))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

model = Regression_Algorithm(learning_rate=0.1, epochs=3000)
model.fit(X_train, y_train)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu JSON từ client
        data = request.get_json()

        # Kiểm tra dữ liệu đầu vào
        required_fields = ['economy', 'gpa', 'absent_days', 'part_time', 'health_status']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Chuyển đổi dữ liệu thành mảng numpy
        input_data = np.array([
            data['economy'],
            data['gpa'],
            data['absent_days'],
            data['part_time'],
            data['health_status']
        ]).reshape(1, -1)

        # Dự đoán kết quả
        prediction = model.predict(input_data)[0]
        result = "Qua môn" if prediction == 1 else "Rớt môn"

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate', methods=['GET'])
def evaluate():
    y_pred = model.predict(X_test)
    accuracy = np.mean(y_pred == y_test) * 100
    return jsonify({"accuracy": f"{accuracy:.2f}%"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

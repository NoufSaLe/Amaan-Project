from flask import Flask, jsonify
from flask_cors import CORS  # مكتبة السماح بالاتصال بين React و Flask

app = Flask(__name__)
CORS(app)  # تفعيل المكتبة

# المسار الرئيسي (اختياري للتأكد أن السيرفر يعمل)
@app.route("/")
def home():
    return "Amaan Project backend is running ✅"

# المسار الذي سيطلبه React لجلب البيانات
@app.route("/api/data")
def get_data():
    return jsonify({"message": "Hello from Flask Backend!"})

if __name__ == "__main__":
    app.run(debug=True)
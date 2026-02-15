from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
import os
from urllib.parse import urlparse
import requests

app = Flask(__name__)
CORS(app)


BLOCKED_SCHEMES = {"javascript", "data", "file"}
# التعديل الصحيح: المفتاح يوضع مباشرة بين علامات تنصيص
VT_API_KEY = "10b27894fc878edab9780d9f288ebb33ddd0e28d21c5ddabe473b1f12925259f"
def analyze_url_basic(input_text: str):
    text = input_text.strip()
    if not text.startswith(("http://", "https://")):
        text = "https://" + text
    
    parsed = urlparse(text)
    result = {
        "is_url": bool(parsed.scheme and parsed.netloc),
        "is_valid_format": True,
        "normalized_url": text,
        "reason": None
    }
    
    if parsed.scheme.lower() in BLOCKED_SCHEMES:
        result["is_valid_format"] = False
        result["reason"] = "BLOCKED_SCHEME"
    
    return result

def check_virustotal(url: str):
    if not VT_API_KEY:
        return {"success": False, "error": "NO_API_KEY"}
    
    headers = {"x-apikey": VT_API_KEY}
    try:
        # إرسال الرابط للفحص
        response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": url})
        if response.status_code != 200:
            return {"success": False, "error": f"VT_ERROR_{response.status_code}"}
        
        # جلب النتائج
        analysis_id = response.json()["data"]["id"]
        analysis_res = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=headers)
        stats = analysis_res.json()["data"]["attributes"]["stats"]
        malicious_count = stats.get("malicious", 0)
        
        return {
            "success": True,
            "malicious": malicious_count > 0,
            "malicious_count": malicious_count
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- المسارات (Routes) ---

@app.route("/")
def home():
    return "Amaan Project backend is running ✅"

@app.route("/api/scan-qr", methods=["POST"])
def scan_qr_api():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "لم يتم اختيار صورة"}), 400
    
    file = request.files['file']
    try:
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            # طباعة الرابط الذي تم استخراجه من الصورة للتأكد
            print(f"\n[INFO] الرابط المستخرج: {data}")
            
            analysis = analyze_url_basic(data)
            vt_result = None
            if analysis["is_valid_format"]:
                vt_result = check_virustotal(analysis["normalized_url"])
                # طباعة نتيجة الفحص القادمة من VirusTotal
                print(f"[INFO] نتيجة VirusTotal: {vt_result}\n")
            
            return jsonify({
                "success": True, 
                "data": data, 
                "analysis": analysis,
                "vt_result": vt_result
            })
        
        print("[WARN] لم يتم العثور على QR في الصورة")
        return jsonify({"success": False, "error": "لم يتم العثور على رمز QR داخل الصورة"}), 200
            
    except Exception as e:
        print(f"[ERROR] حدث خطأ: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# تأكدي أن هذا السطر دائماً في نهاية الملف
if __name__ == "__main__":
    app.run(debug=True)
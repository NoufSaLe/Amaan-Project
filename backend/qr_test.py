import cv2
from urllib.parse import urlparse
from Blacklist import check_virustotal

BLOCKED_SCHEMES = {"javascript", "data", "file"}

def decode_qr(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return {"success": False, "data": None, "error": "IMAGE_NOT_READABLE"}

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if points is None or data.strip() == "":
        return {"success": False, "data": None, "error": "QR_NOT_FOUND"}

    return {"success": True, "data": data.strip(), "error": None}


def analyze_url_basic(input_text: str):
    result = {
        "is_url": False,
        "is_valid_format": False,
        "normalized_url": None,
        "reason": None
    }

    if not input_text or not isinstance(input_text, str):
        result["reason"] = "EMPTY_INPUT"
        return result

    text = input_text.strip()

    # لو ما فيه http/https نضيف https كبداية
    if not text.startswith(("http://", "https://")):
        text = "https://" + text

    parsed = urlparse(text)

    # لازم scheme + netloc
    if not parsed.scheme or not parsed.netloc:
        result["reason"] = "NOT_A_URL"
        return result

    # منع schemes الخطرة
    if parsed.scheme.lower() in BLOCKED_SCHEMES:
        result["reason"] = "BLOCKED_SCHEME"
        return result

    # تحقق بسيط: ما فيه مسافات
    if " " in parsed.netloc:
        result["reason"] = "INVALID_NETLOC"
        return result

    result["is_url"] = True
    result["is_valid_format"] = True
    result["normalized_url"] = text
    return result


if __name__ == "__main__":
    qr_res = decode_qr("unsafe1.png")
    print("QR RESULT:", qr_res)

    if qr_res["success"]:
        analysis = analyze_url_basic(qr_res["data"])
        print("URL ANALYSIS:", analysis)

        if analysis["is_valid_format"]:
            vt_result = check_virustotal(analysis["normalized_url"])
            print("VT RESULT:", vt_result)
    else:
        print("Stop - QR error:", qr_res["error"])
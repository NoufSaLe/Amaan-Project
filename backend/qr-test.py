import cv2

def decode_qr(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return {"success": False, "data": None, "error": "IMAGE_NOT_READABLE"}

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if points is None or data.strip() == "":
        return {"success": False, "data": None, "error": "QR_NOT_FOUND"}

    return {"success": True, "data": data.strip(), "error": None}


if __name__ == "__main__":
    print(decode_qr("QRtest.jpg"))
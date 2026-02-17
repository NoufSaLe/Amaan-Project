from qr_test import decode_qr, analyze_url_basic
from Blacklist import check_virustotal
from phishtank import check_phishtank


def scan_pipeline(image_path: str):
    """
    Full QR scanning pipeline:
    QR -> URL validation -> VirusTotal -> PhishTank
    """

    # 1️ Decode QR
    qr_res = decode_qr(image_path)
    if not qr_res["success"]:
        return qr_res

    # 2️ Analyze URL
    analysis = analyze_url_basic(qr_res["data"])
    if not analysis["is_valid_format"]:
        return {
            "success": False,
            "stage": "url_validation",
            "details": analysis
        }

    # 3️ VirusTotal check
    vt_result = check_virustotal(analysis["normalized_url"])

    # 4️ PhishTank check
    phish_result = check_phishtank(analysis["normalized_url"])

    #  Final unified result
    return {
        "success": True,
        "qr_data": qr_res["data"],
        "url": analysis["normalized_url"],
        "virustotal": vt_result,
        "phishtank": phish_result
    }

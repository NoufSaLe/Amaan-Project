import os
import requests

VT_API_KEY = os.getenv("VT_API_KEY")

def check_virustotal(url: str):
    if not VT_API_KEY:
        return {
            "success": False,
            "malicious": None,
            "error": "NO_API_KEY"
        }

    headers = {
        "x-apikey": VT_API_KEY
    }

    params = {
        "url": url
    }

    try:
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data=params
        )

        if response.status_code != 200:
            return {
                "success": False,
                "malicious": None,
                "error": f"VT_ERROR_{response.status_code}"
            }

        result = response.json()

        analysis_id = result["data"]["id"]

        # نجيب النتيجة
        analysis_response = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        analysis_data = analysis_response.json()

        stats = analysis_data["data"]["attributes"]["stats"]

        malicious_count = stats.get("malicious", 0)

        return {
            "success": True,
            "malicious": malicious_count > 0,
            "malicious_count": malicious_count,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "malicious": None,
            "error": str(e)
        }
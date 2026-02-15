# phishtank.py

DB_PATH = "phishtank_db.txt"


def load_phishing_db():
    """
    Load phishing URLs from local dataset
    """

    phishing_urls = set()

    with open(DB_PATH, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url:
                phishing_urls.add(url)

    return phishing_urls



PHISHTANK_URLS = load_phishing_db()


def check_phishtank(url: str):
    """
    Check if URL exists in local phishing database
    """

    try:
        is_phishing = url.strip() in PHISHTANK_URLS

        return {
            "success": True,
            "phishing": is_phishing,
            "source": "local_phishing_dataset",
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "phishing": None,
            "error": str(e)
        }

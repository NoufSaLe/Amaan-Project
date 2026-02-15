import pandas as pd
import re
from urllib.parse import urlparse

# =========================
# Read dataset
# =========================
df = pd.read_csv("dataset_url_label.csv")
df.columns = [c.strip().lower() for c in df.columns]

# Check required columns
if "url" not in df.columns or "label" not in df.columns:
    raise ValueError("Dataset must contain 'url' and 'label' columns")

# =========================
# Data cleaning
# =========================
df = df.dropna(subset=["url", "label"]).copy()

df["url"] = df["url"].astype(str).str.strip()
df["url"] = df["url"].str.replace(r"\s+", "", regex=True)
df = df[df["url"] != ""]

df["label"] = pd.to_numeric(df["label"], errors="coerce")
df = df[df["label"].isin([0, 1])]

before = len(df)
df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
after = len(df)

print("Total URLs after cleaning:", after)
print("Removed duplicates:", before - after)
print(df["label"].value_counts())

# =========================
# Feature extraction
# =========================
SUSPICIOUS_KEYWORDS = [
    "login","verify","verification","account","secure","update",
    "signin","bank","payment","pay","crypto","wallet",
    "confirm","password","reset","authorize","billing"
]

SPECIAL_CHARS = r"[@!#$%^&*()+=\[\]{}|\\:;\"'<>,?/`~_-]"
REDIRECT_KEYWORDS = ["redirect=", "url=", "next=", "return="]

def has_suspicious_keywords(url):
    return int(any(k in url.lower() for k in SUSPICIOUS_KEYWORDS))

def safe_urlparse(url):
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "http://" + url
    return urlparse(url)

def extract_features(url):
    parsed = safe_urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    url_length = len(url)
    hostname_length = len(hostname)
    path_length = len(path)

    dots_count = hostname.count(".")
    parts = hostname.split(".") if hostname else []
    subdomains_count = max(len(parts) - 2, 0)

    digits_count = len(re.findall(r"\d", url))
    query_length = len(query)
    query_params_count = 0 if query == "" else len(query.split("&"))

    double_slash_redirects = max(url.count("//") - 1, 0)
    keyword_redirects = sum(url.lower().count(k) for k in REDIRECT_KEYWORDS)
    redirect_count = double_slash_redirects + keyword_redirects

    special_chars_count = len(re.findall(SPECIAL_CHARS, url))
    special_chars_ratio = special_chars_count / url_length if url_length > 0 else 0

    uses_https = int(parsed.scheme.lower() == "https")
    has_ip = int(bool(re.search(r"(\d{1,3}\.){3}\d{1,3}", hostname)))
    has_port = int(parsed.port is not None)

    encoding_symbols_count = url.count("%")

    return pd.Series({
        "url_length": url_length,
        "hostname_length": hostname_length,
        "path_length": path_length,
        "dots_count": dots_count,
        "subdomains_count": subdomains_count,
        "digits_count": digits_count,
        "query_length": query_length,
        "query_params_count": query_params_count,
        "redirect_count": redirect_count,
        "special_chars_ratio": special_chars_ratio,
        "has_ip": has_ip,
        "has_port": has_port,
        "uses_https": uses_https,
        "has_suspicious_keywords": has_suspicious_keywords(url),
        "encoding_symbols_count": encoding_symbols_count
    })

features_df = df["url"].apply(extract_features)

final_df = pd.concat([df[["url"]], features_df, df[["label"]]], axis=1)

final_df.to_csv("dataset_features_15.csv", index=False)

print("Process completed successfully")
print("Final dataset shape:", final_df.shape)

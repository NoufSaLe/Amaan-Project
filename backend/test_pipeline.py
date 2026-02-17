from pipeline import scan_pipeline

# نشغل الفحص على صورة QR
result = scan_pipeline("unsafe1.png")

print("\n=== FINAL RESULT ===")
print(result)

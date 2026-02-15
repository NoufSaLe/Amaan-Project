import qrcode

url = "http://00003485.com/banks/tangerine"

img = qrcode.make(url)
img.save("unsafe1.png")

print("QR created!")
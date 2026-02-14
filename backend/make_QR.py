import qrcode

url = "https://secure.eicar.org/eicar.com.txt"

img = qrcode.make(url)
img.save("unsafe1.png")

print("QR created!")
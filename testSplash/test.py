import requests

a = requests.get("https://www.foody.vn/ha-noi/hoa-qua-dam-pho-to-tich/binh-luan")
print(a.text)
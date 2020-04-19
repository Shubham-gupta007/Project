import requests

res = requests.get('https://google.com')

print(res.headers)
if res:
    print('Response Ok')
else:
    print('Response Failed')
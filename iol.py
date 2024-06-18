import json
import requests

url_iol = 'https://api.invertironline.com/'

headers = { 'Content-Type':'application/x-www-form-urlencoded' }
body = dict(
                username='jelopez@gmail.com',
                password='S.',
                grant_type='password'
            )

response = requests.post(f"{url_iol}/token",headers=headers, data=body)

print(response)
print(response.status_code)
print(response)


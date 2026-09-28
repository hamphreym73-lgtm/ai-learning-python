import requests

url = "https://httpbin.org/get"

try:
    response = requests.get(url, timeout=5)

    response.raise_for_status()

    data = response.json()

    print("success")
    print(data)

except requests.exceptions.RequestException as e:
    print("fail", e)
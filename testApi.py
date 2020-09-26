import requests

BASE = "http://localhost:4080/"

print(requests.get(BASE + "health").text)
print(requests.post(BASE + "convert/XX").text)
print(requests.get(BASE + "diag").text)
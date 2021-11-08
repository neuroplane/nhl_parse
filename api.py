import requests

url = "https://x125.ru/api/neurotlg/teletest"

payload = {"items": "text"}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 11609376-ff57-401e-88a4-53f4c0904fdb"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
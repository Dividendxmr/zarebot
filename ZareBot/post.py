import requests, json

def main():
    url = "https://manager.zare.com/api/v1/dedicated"
    headers = {
    'Authorization': "vXuZ7Kt2ri6SsmoTR3sZU6xUkFme7gub",
    }
    body = {
        'server_id': '1474921336'
    }

    resp = requests.post(url, headers=headers, data=body)

    jsonResponse = resp.json()
    
    print(jsonResponse)
main()

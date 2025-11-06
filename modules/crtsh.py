import requests

def search_crt(target):
    url = f"https://crt.sh/?q=%25.{target}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
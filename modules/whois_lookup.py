import whois
import requests
import socket


def buscar_whois(dominio):
    try:
        w = whois.whois(dominio)
        return {
            "dominio" : dominio,
            "registrante" : w.name,
            "email" : w.emails,
            "pais" : w.country,
            "data_criacao" : w.creation_date,
        }
    except Exception as e:
        return {"erro": str(e)}
    
def geolocalizar (dominio):
    ip = socket.gethostbyname(dominio)
    url = f"https://ipinfo.io{ip}/json"
    r = requests.get(url).json()
    return{
        "IP" : ip,
        "Local" : r.get("city") + ", " + r.get("region") + ", " + r.get("country"),
        "Org" : r.get("org"),
    }
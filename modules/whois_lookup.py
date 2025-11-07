import os
import socket
import time
from typing import Any, Dict, Optional

import whois
import requests

def _retry(fn, attempts: int = 3, base_delay:float = 0.5, *args, **kwargs):
    """
    Helper simples para retries com backoff exponencial.
    fn: callable
    attempts: número total de tentativas
    base_delay: atraso inicial (em segundos), dobra a cada tentativa
    """

    delay = base_delay
    last_exec = None
    for i in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_exec = e
            if i == attempts:
                raise
            time.sleep(delay)
            delay *= 2
    raise last_exec

def buscar_whois(dominio:str, attempts: int = 2, timeout: float = 10.0) -> Dict[str, Any]:
    """
    Consulta WHOIS de forma resiliente.
    Retorna dicionário com campos previsiveis ou campo 'erro_*' em caso de falha
    """
    dominio = dominio.strip()
    if not dominio:
        return{"erro_input": "domínio vazio"}

    def _call_whois():
        #whois.whois pode lançar exceções ou retornar objetos parcias
        return whois.whois(dominio)
    
    try:
        w = _retry(_call_whois, attempts)
    except Exception as e:
        return {"Erro whois": str(e)}

    def _norm(val: Optional[Any]) -> Any:
        if val is None:
            return "Desconhecido"
        return val

    try:
        name = _norm(getattr(w, "name", None))
        emails = getattr(w, "emails", None)
        if isinstance(emails, (list, tuple)):
            emails = ", ".join(str(e) for e in emails if e)
        emails = _norm(emails)
        country = _norm(getattr(w, "country", None))
        creation = getattr(w, "creation_date", None)
        if isinstance(creation, (list, tuple)):
            creation = creation[0] if creation else None
        creation = _norm(str(creation)) if creation is not None else "Desconhecida"

        return {
            "dominio": dominio,
            "registrante": name,
            "email": emails,
            "pais": country,
            "data_criacao": creation,
        }
    except Exception as e:
        return {"erro_parsing_whois": str(e)}


def _consulta_ipinfo(ip: str, token: Optional[str], timeout: float) -> Dict[str, Any]:
    """
    Consulta ipinfo.io (requer token opcional). Lança exceção em caso de falha.
    """
    url = f"https://ipinfo.io/{ip}/json"
    params = {}
    if token:
        params["token"] = token
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _consulta_ip_api(ip: str, timeout: float) -> Dict[str, Any]:
    """
    Consulta ip-api.com (fallback, sem token). Lança exceção em caso de falha.
    """
    url = f"http://ip-api.com/json/{ip}"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def geolocalizar(
    dominio: str,
    timeout: float = 5.0,
    attempts: int = 2,
    base_delay: float = 0.5,
) -> Dict[str, Any]:
    """
    Resolve domínio -> IP e tenta obter geolocalização de forma resiliente.
    Usa ipinfo.io (com token opcional via env IPINFO_TOKEN) e como fallback ip-api.com.
    Retorna dicionário com chave 'erro_*' em caso de problemas.
    """

    dominio = dominio.strip()
    if not dominio:
        return {"erro_input": "domínio vazio"}

    try:
        def _resolve():
            return socket.gethostbyname(dominio)

        ip = _retry(_resolve, attempts=attempts, base_delay=base_delay)
    except Exception as e:
        return {"erro_resolver_ip": str(e)}

    session = requests.Session()
    token = os.environ.get("IPINFO_TOKEN")  # opcional

    try:
        def _call_ipinfo():
            return _consulta_ipinfo(ip, token, timeout)

        dados = _retry(_call_ipinfo, attempts=attempts, base_delay=base_delay)
        cidade = dados.get("city") or "Desconhecida"
        regiao = dados.get("region") or "Desconhecida"
        pais = dados.get("country") or "Desconhecido"
        org = dados.get("org") or "Desconhecida"
        return {
            "IP": ip,
            "Local": f"{cidade}, {regiao}, {pais}",
            "Org": org,
            "Fonte": "ipinfo.io",
        }
    except Exception as e_ipinfo:
        print(f"[WARN] ipinfo falhou: {e_ipinfo}. Tentando fallback ip-api.com...")

    try:
        def _call_ip_api():
            return _consulta_ip_api(ip, timeout)

        dados2 = _retry(_call_ip_api, attempts=attempts, base_delay=base_delay)
        cidade = dados2.get("city") or "Desconhecida"
        regiao = dados2.get("regionName") or dados2.get("region") or "Desconhecida"
        pais = dados2.get("country") or "Desconhecido"
        org = dados2.get("org") or dados2.get("isp") or "Desconhecida"
        return {
            "IP": ip,
            "Local": f"{cidade}, {regiao}, {pais}",
            "Org": org,
            "Fonte": "ip-api.com",
        }
    except Exception as e_ipapi:
        return {"erro_geolocalizacao": f"ipinfo: {e_ipinfo}; ip-api: {e_ipapi}"}

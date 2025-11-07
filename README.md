# Network Scanner Tool — Guia de Uso

Este README **apenas** explica como usar a ferramenta. (Implementação e correção de erros estão por vir em breve.)

---

## Estrutura mínima do repositório

```
main.py                 # CLI principal
modules/
  crtsh.py              # busca de certificados (crt.sh)
  dir_enum.py           # enumeração de diretórios
  port_scanner.py       # scanner de portas
  whois_lookup.py       # whois e geolocalização
```

---

## Pré-requisitos rápidos

* Python 3.8+ instalado.
* Recomendo criar um virtualenv: `python -m venv venv` e ativá-lo.
* Instale dependências básicas (ex.: `requests`, `python-whois`) quando subir o `requirements.txt`.

---

## Como executar a ferramenta

Execute a partir do diretório do projeto:

```bash
python main.py <comando> [argumentos...]
```

Se nenhum comando válido for passado, a ajuda (usage) será exibida.

### Comandos suportados

1. **crtsh** — Buscar certificados relacionados a um domínio (usa crt.sh)

```bash
python main.py crtsh example.com
```

* `example.com` — domínio alvo.
* Saída esperada: JSON/lista de entradas retornadas pelo crt.sh (ou mensagem de erro).

2. **dir_enum** — Enumeração de diretórios a partir de uma wordlist

```bash
python main.py dir_enum example.com /caminho/wordlist.txt
```

* `example.com` — alvo (hostname).
* `/caminho/wordlist.txt` — arquivo com palavras (uma por linha) para testar caminhos.
* Saída esperada: lista de diretórios encontrados (ex.: `/admin`, `/login`).

3. **port_scan** — Scanner de portas TCP

```bash
python main.py port_scan 192.168.1.10 22 80 443 8080
```

* `192.168.1.10` — IP ou hostname alvo.
* `22 80 443` — lista de portas (inteiros) a serem verificadas.
* Saída esperada: lista ou dicionário de portas abertas (ex.: `22: open`).

4. **whois** — Consulta WHOIS para um domínio

```bash
python main.py whois example.com
```

* Saída esperada: campos principais do WHOIS (registrante, email, data de criação etc.) em formato legível.

5. **geo** — Geolocalização de IP/domínio (usa ipinfo/ip-api)

```bash
python main.py geo example.com
```

* Pode usar a variável de ambiente `IPINFO_TOKEN` para melhorar limites de consulta em ipinfo.io.
* Saída esperada: IP resolvido, cidade, região, país, organização e fonte da informação.

---

## Formato de saída no CLI

O `main.py` imprime os resultados retornados pelos módulos com regras simples:

* `dict` → cada chave: valor em linha separada.
* `list` → um item por linha.
* `str` ou outros → impressão direta do conteúdo.
* `None` ou lista vazia → exibe: `Nenhum resultado encontrado`.


---

## Exemplos rápidos

```bash
# certificados
python main.py crtsh example.com

# enumeração de diretórios usando wordlist pequena
python main.py dir_enum example.com ./wordlists/common.txt

# varredura de portas específica
python main.py port_scan scanme.nmap.org 22 80 443

# whois e geo
python main.py whois example.com
python main.py geo example.com
```

---

## Variáveis de ambiente úteis

* `IPINFO_TOKEN` — token opcional para `ipinfo.io` (usado pela função de geolocalização). Se não informado, a ferramenta tentará um fallback (ip-api).

---

## Observações e boas práticas ao usar

* Use a ferramenta apenas em alvos autorizados. Varreduras e enumerações sem permissão podem ser ilegais.
* Para `port_scan` em redes públicas, ajuste tempos/timeouts e, se necessário, execute com permissões apropriadas.
* Para `dir_enum` use wordlists respeitáveis e evite sobrecarregar o alvo (rate limit).

---

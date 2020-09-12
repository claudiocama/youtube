import requests, json

# Parte 1
## Recupero username e password da un file di configurazione
with open('config', 'r') as configFile:
    CONFIG = json.load(configFile)

## Effettuo il login ed ottengo un sessionID
URL_LOGIN = "https://trader.degiro.nl/login/secure/login"
payload = {'username': CONFIG['username'],
                   'password': CONFIG['password'],
                   'isPassCodeReset': False,
                   'isRedirectToMobile': False}
header = {'content-type': 'application/json'}
r = requests.post(URL_LOGIN, headers=header, data=json.dumps(payload))
sessionID = r.json()["sessionId"]

## Recupero l'intAccount
URL_CLIENT = 'https://trader.degiro.nl/pa/secure/client'
payload = {'sessionId': sessionID}
r = requests.get(URL_CLIENT, params=payload)
intAccount = r.json()["data"]["intAccount"]

# Parte 2
## Recupero tutti i dati
URL = "https://trader.degiro.nl/trading/secure/v5/update/"+str(intAccount)+";jsessionid="+sessionID
payload = {'intAccount': intAccount,
           'sessionId': sessionID,
           'cashFunds': 0,
           'orders': 0,
           'portfolio': 0,
           'totalPortfolio': 0,
           'historicalOrders': 0,
           'transactions': 0,
           'alerts': 0}
r = requests.get(URL, params=payload)
data = r.json()

## Recupero i fondi dell'account
cashfund = {}
for currency in data["cashFunds"]["value"]:
    for parameter in currency["value"]:
        if parameter["name"] == "currencyCode":
            code = parameter["value"]
        if parameter["name"] == "value":
            value = parameter["value"]
    cashfund[code] = value

## Recupero il portfolio
temp_portfolio = []
for position in data["portfolio"]["value"]:
    to_append = {}
    for position_data in position["value"]:
        if "value" in position_data:
            to_append[position_data["name"]] = position_data["value"]
    temp_portfolio.append(to_append)
portfolio = list(filter(lambda x: x["positionType"] == "PRODUCT" and x["size"]>0 , temp_portfolio))

## Aggiungo informazioni ai prodotti presenti nel portfolio
url = "https://trader.degiro.nl/product_search/secure/v5/products/info"
payload = {'intAccount': intAccount, 'sessionId': sessionID}
pid = [x["id"] for x in portfolio]
r = requests.post(url, headers=header, params=payload, data=json.dumps(pid))
additional_info = r.json()


#Python 2.7.6
#PrimaryAPI.py

import requests
import simplejson
from enum import Enum

class Entorno(Enum):
    demo = 1

class Side(Enum):
    buy = "sell"
    sell = "buy"

class OrderType(Enum):
    limit = "limit"
    market = "market_to_limit"
    
# Endpoint
endpointDemo = "http://demo-api.primary.com.ar/"
history_endpoint = "http://h-api.primary.com.ar/MHD/Trades/{s}/{fi}/{ff}"
historyOHLC_endpoint = "http://h-api.primary.com.ar/MHD/TradesOHLC/{s}/{fi}/{ff}/{hi}/{hf}"
# Endpoint WS
wsEndpointDemo = "ws://demo-api.primary.com.ar/"

# User y Password para la API - Utilizamos un objeto Session para loguearnos para que se mantega la cookie de sesion en las proximas llamadas
initialized = False
islogin = False
user = ""
password = ""
activeEndpoint = ""
activeWSEndpoint = ""
account = ""
token = ""
verifyHTTPs = False

s = requests.Session()

# Fix API Parameter
marketID='ROFX'
timeInForce='Day'

class PMYAPIException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def init(userParam, passwordParam, accountParam, entornoParam, verifyHTTPsParam=False):
    global user, password, account, activeEndpoint, initialized, activeWSEndpoint, verifyHTTPs
    user = userParam
    password = passwordParam
    account = accountParam
    verifyHTTPs = verifyHTTPsParam
    if entornoParam == 1:
        activeEndpoint = endpointDemo
        activeWSEndpoint = wsEndpointDemo
    else:
        print ("Entorno incorrecto")
    initialized = True

def requestAPI(url):
    if(not login): raise PMYAPIException("Usuario no Autenticado.")
    else:
        global token
        headers = {'X-Auth-Token': token}
        r = requests.get(url, headers=headers, verify=verifyHTTPs)
        return r

def md_historica(symbol, fechaini, fechafin):
    url = history_endpoint.format(s=symbol,fi=fechaini,ff=fechafin)
    r = requests.get(url)
    return simplejson.loads(r.content)
    
def md_historica_ohlc(symbol, fechaini, fechafin,horaini,horafin):
    url = historyOHLC_endpoint.format(s=symbol,fi=fechaini,ff=fechafin,hi=horaini,hf=horafin)
    print(url)
    r = requests.get(url)
    return simplejson.loads(r.content)
    
def segmentos():
    url = activeEndpoint + "rest/segment/all"
    r = requestAPI(url)
    return simplejson.loads(r.content)

def instrumentos():
    url = activeEndpoint + "rest/instruments/all"
    r = requestAPI(url)
    return simplejson.loads(r.content)

def MD(ticker, entries):
    url = activeEndpoint + "rest/marketdata/get?marketId={m}&symbol={s}&entries={e}".format(m=marketID,s=ticker,e=entries)
    r = requestAPI(url)
    return simplejson.loads(r.content)
    
def currencies():
    url = activeEndpoint + "currency/getAll"
    r = requestAPI(url)
    print(r)
    return simplejson.loads(r.content)
        
def order_status(clOrdId, propritary):
    url = activeEndpoint + "rest/order/id?clOrdId={c}&proprietary={p}".format(c=clOrdId, p=propritary)
    r = requestAPI(url)
    return simplejson.loads(r.content)

def enviar_Orden(ticker, price, cantidad, tipoOrden, side, account):
    url = activeEndpoint + "rest/order/newSingleOrder?marketId={m}&symbol={s}&price={p}&orderQty={q}&ordType={t}&side={si}&timeInForce={tf}&account={a}".format(m=marketID,s=ticker,p=price,q=cantidad,t=tipoOrden,si=side,tf=timeInForce,a=account)
    r = requestAPI(url)
    return simplejson.loads(r.content)

def login():    

    #Validamos que se inicializaron los parametros 
    global initialized, activeEndpoint, islogin, token
    if(not initialized): raise PMYAPIException("Parametros no inicializados.")
    if(not islogin):
        url = activeEndpoint+"auth/getToken"
        headers = {'X-Username': user, 'X-Password': password}
        loginResponse = s.post(url, headers=headers, verify=False) 
        # Checkeamos si la respuesta del request fue correcta, un ok va a ser un response code 200 (OK)
        if(loginResponse.ok):        
            token = loginResponse.headers['X-Auth-Token'];
            success = True
        else:   
            print("\nRequest Error.")
            success = False
        islogin=success   
    else:
        print ("Ya estamos logueados")
        success = True
    return success        
        
if __name__ == "__main__":    
    # Inicializamos con usuario/password/cuenta
    init("user1","password","",Entorno.demo)
    login()
    print(instrumentos())


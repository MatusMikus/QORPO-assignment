from aiohttp import web, ClientSession
from sqlalchemy import select
import base64
import time
import hmac
import hashlib
import models

async def default(request):
    return web.Response(text="The valid endpoints are /price/history or /price/{currency}")


async def get_price_handler(request):
    endpoint = request.match_info['endpoint']
    if(endpoint == 'history'):
        return await get_price(request)
    else:
        return await get_coin(request)
    
async def get_price(request):
    pageSize = 50
    offset = 0
    try:
        offset = pageSize * int(request.query.get('page',0))
    except:
        pass
    with request.app['db'].connect() as conn:
        cols = models.price.columns
        selection = select([cols.currency, cols.date, cols.price])
        cursor = conn.execute(selection
            .limit(pageSize)
            .offset(offset))
        records = cursor.fetchall() 
        prices = [dict(q) for q in records]
        return web.Response(text=str(prices))

async def get_coin(request):
    coin = request.match_info['endpoint']
    if(coin == None):
        return web.Response(text="no coin found")

    coinSymbol = coin + "-USDT"
    params = {
        'symbol': coinSymbol
    }
    kucoin_conf = request.config_dict['config']['kucoin']
    api_key = kucoin_conf['api_key'] 
    api_secret = kucoin_conf['api_secret']
    api_passphrase = kucoin_conf['api_passphrase']

    url = 'https://api.kucoin.com/api/v1/market/stats'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/market/stats'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature.decode('utf-8'),
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase.decode('utf-8'),
        "KC-API-KEY-VERSION": "2"
    }

    async with ClientSession() as session:
        async with session.get(url,params=params,headers=headers) as resp:
            testcoin = "btc"
            json = await resp.json()
            data = json.get('data', None)
            lastBid = data['last'] if data else ['No bid found']
            coinString = "TEST bid for %s:" % testcoin
            return web.Response(text=coinString + str(lastBid))
            

from datetime import date, datetime
from sqlalchemy.sql.sqltypes import String
from aiohttp import web, ClientSession
from sqlalchemy import select, cast, Date
import models
import ccxt


async def default(request):
    return web.Response(text="The valid endpoints are /price/history or /price/{currency}")


async def get_price_handler(request):
    endpoint = request.match_info['endpoint']
    if(endpoint == 'history'):
        return await get_price(request)
    else:
        return await get_coin(request)
    
async def get_price(request):
    if not request.app['db']:
        return web.Response(text="Error: couldn't connect to database")
    pageSize = 50
    offset = 0
    try:
        offset = pageSize * int(request.query.get('page',0))
    except:
        pass
    cols = models.price.columns 
    selection = select([cols.currency, cols.date.cast(String), cols.price])
    
    cursor = request.app['db_connect'].execute(selection
                            .limit(pageSize)
                            .offset(offset))
    records = cursor.fetchall() 
    prices = [dict(q) for q in records]
    return web.Response(text=str(prices))

async def get_coin(request):
    coin = request.match_info['endpoint']
    if(coin == None):
        return web.Response(text="no coin found")

    ccxtTicker = coin + '/USDT'
    try:
        ccxtResponse = ccxt.kucoin().fetchTicker(ccxtTicker)
    except:
        return web.Response(text="error: didn't find coin {} on kucoin".format(coin))
    ccxtOutput = ccxtResponse['last']

    coinString = "Last bid for {}:  {}\n".format(coin, str(ccxtOutput))
    return web.Response(text=coinString)
    
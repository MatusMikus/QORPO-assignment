from aiohttp import web
from controllers import default, get_price_handler
from config import config, context

app = web.Application()
app.add_routes([web.get('/',default)])
app.add_routes([web.get('/price/{endpoint}', get_price_handler)])
app['config'] = config
app.cleanup_ctx.append(context)

web.run_app(app)
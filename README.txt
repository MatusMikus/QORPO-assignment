Database name is configured through config.yaml

Some thoughts behind my decisions:

- switched from MySQL to SQLite to include the database with the rest of the API. The DB will still be created if it doesn't exist. SQLite is also designed for a single connection, so I didn't implement pooling.

- I have tried to address the database through middleware, but online research showed that database transactions should be done in controllers instead of middleware, plus middleware touches all handlers, and we don't need to access the database for the kucoin api, so I kept that part of the API the same. I'd be interested in learning how the database middleware should be handled, since it's possible I'm misunderstanding something

- for the /price/history endpoint, I have populated the MySQL database with the historical data of 3 coins: BTC, ETH, and LTC. They are added sequentially, so the first 1500 rows or so are BTC, the next 1500 or so ETH and so on

- to run through gunicorn, 'gunicorn main:app --worker-class aiohttp.worker.GunicornWebWorker' should work
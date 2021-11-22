Note: Assume a MySQL server is running and configured through a 'config.yaml' file, based on 'config_sample.yaml'. Otherwise the history endpoint won't work. I have used MySQL Workbench/Server for testing on localhost, there's proof of a working example in the misc directory

Some thoughts behind my decisions:

- switched from MySQL to SQLite to include the database with the rest of the API. The DB will still be created if it doesn't exist 

- I didn't see a need to use middleware, since we're not intercepting handlers. I can see the point of using middleware for writing custom 404s and 500s, but decided it wasn't necessary

- I have initially missed the requirement to use for the ccxt library so I made a new KuCoin account and made the requests go through their official API. I'm keeping the original code commented out in the same request handler as a comparison

- for the /price/history endpoint, I have populated the MySQL database with the historical data of 3 coins: BTC, ETH, and LTC. They are added sequentially, so the first 1500 rows or so are BTC, the next 1500 or so ETH and so on

- to run through gunicorn, 'gunicorn main:app --worker-class aiohttp.worker.GunicornWebWorker' should work
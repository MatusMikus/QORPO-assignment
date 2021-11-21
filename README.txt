Some thoughts behind my decisions:

- I didn't see a need to use middleware, since we're not intercepting handlers. I can see the point of using middleware for writing custom 404s and 500s, but decided it wasn't necessary

- I have initially missed the requirement to use for the ccxt library so I made a new KuCoin account and made the requests go through their official API. I'm keeping the original code commented out in the same request handler as a comparison

- for the /price/history endpoint, I have populated a MySQL database with the historical data of 3 coins: BTC, ETH, and LTC. I have added them sequentially, so the first 1500 rows or so are BTC, the next 1500 or so ETH and so on

- We assume the database is present on localhost with credentials as in the sample config. Same for KuCoin API, but that is optional
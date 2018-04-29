import asyncio
import datetime
import pickle

import binance
from apikeyfilegenerator import ApiKeyFileGenerator

# Turn logging on, its off by default
DECODE_PW = 'c2_pw%&_23'
binance.enable_logging(True)

# obtain from file the binance encoded API keys. This file was created using
# ApiKeyFileGenerator.
with open(ApiKeyFileGenerator.FILE_PATH + 'bi.bin', 'rb') as handle:
    encryptedKeyList = pickle.load(handle)

ap = ApiKeyFileGenerator()

# decode the keys with the pw used to encode them
api_key = ap.decode(DECODE_PW, encryptedKeyList[0])
api_secret_key = ap.decode(DECODE_PW, encryptedKeyList[1])


def market_data():
    print("\n-------- Market data examples --------\n")

    # ping binance to see if it's online and verify we can hit it
    print("Connection ok? ", binance.ping())

    # Get the current server time in milliseconds
    print("Server time: ", binance.server_time())

    # Get the order book for a symbol with max 5 entries
    order_book = binance.order_book("BNBBTC", 5)
    print(order_book)


    print("Order book for BNB-BTC")
    print("asks")
    for (price, quantity) in order_book.asks:
        print(price, quantity)

    print("bids")
    for (price, quantity) in order_book.bids:
        print(price, quantity)


    # Get aggregated trades
    print(binance.aggregate_trades("BNBBTC", limit=5))

    candles = binance.candlesticks("BNBBTC", "1m")
    print(candles)

    # Ticker operations
    print("Current ticker prices")
    prices = binance.ticker_prices()
    print(prices)

    print("Current ticker for order books")
    order_books = binance.ticker_order_books()
    print(order_books["ETHBTC"])

    print("Order book ticker for ETHBTC")
    book = order_books["ETHBTC"]
    print(book)

    print("Order book ticker for BNBBTC")
    book = order_books["BNBBTC"]
    print(book)


    last_24hr = binance.ticker_24hr("BNBBTC")
    print(last_24hr)


def account():
    print("\n-------- Account data examples --------\n")

    # For signed requests we create an Account instance and give it the api key and secret
    account = binance.Account(api_key, api_secret_key)

    account.set_receive_window(5000)

    # new_order = account.new_order("ETHBTC", "BUY", "LIMIT", .1, 0.01)
    # new_order_id = new_order["orderId"]
    # print("new order id = ", new_order_id)
    #
    # order = account.query_order("ETHBTC", new_order_id)
    # print(order)
    #
    # order = account.cancel_order("ETHBTC", new_order_id)
    # print(order)

    open_orders = account.open_orders("MCOBTC")
    print(open_orders)

    all_orders = account.all_orders("MCOBTC")
    print(all_orders)

    info = account.account_info()
    print(info)

    trades = account.my_trades("MCOBTC")
    print(trades)


def user_stream():
    print("\n-------- User Stream examples --------\n")

    stream = binance.Streamer()

    async def stop():
        await(asyncio.sleep(5))
        stream.close_all()
        asyncio.get_event_loop().stop()

    def on_user_data(data):
        print("new user data: ", data)

    stream.start_user(api_key, on_user_data)

    asyncio.Task(stop())

    asyncio.get_event_loop().run_forever()

def data_streams():
    print("\n-------- Data Stream examples --------\n")

    stream = binance.Streamer()

    async def stop():
        startTime = datetime.datetime.now()
        print('Starting receiving RT data at {}'.format(startTime.strftime('%H:%M:%S')))
        await(asyncio.sleep(20))
        stream.close_all()
        asyncio.get_event_loop().stop()
        endTime = datetime.datetime.now()
        print('Received RT data from {} to {}'.format(startTime.strftime('%H:%M:%S'), endTime.strftime('%H:%M:%S')))

    def on_order_book(data):
        print("order book changes - ", data)
        print("full orderbook - ", stream.get_order_book("ETHBTC"))

    stream.add_order_book("ETHBTC", on_order_book)


    def on_candlestick(data):
        '''
        Candlestick data format
            {'t': 1525019820000,start time
            'T': 1525019879999, end time
            's': 'ETHBTC',
            'i': '1m',
            'f': 57326037,      first trade number
            'L': 57326183,      last trade number
            'o': '0.07282300',
            'c': '0.07290700',
            'h': '0.07293300',
            'l': '0.07279800',
            'v': '48.57300000', volume
            'n': 147,           number of trades
            'x': False,
            'q': '3.53912310',  quote asset volume (volume in quotation currency, i.e. in BTC)
            'V': '25.57800000', taker buy base asset volume
            'Q': '1.86451044',  taker buy quote asset volume
            'B': '0'}}

        :param data:
        :return:
        '''
        print("new candlesticks - ", data)
        print("all candlesticks- ", stream.get_candlesticks("ETHBTC"))

    stream.add_candlesticks("ETHBTC", "1m", on_candlestick)


    def on_trades(data):
        print("trade update - ", data)

    stream.add_trades("ETHBTC", on_trades)

    asyncio.Task(stop())

    asyncio.get_event_loop().run_forever()


market_data()
#account()
user_stream()
data_streams()
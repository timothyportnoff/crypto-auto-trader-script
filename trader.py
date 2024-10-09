import urllib.parse
import hashlib
import hmac
import base64
import config
import requests
import json
import time
from datetime import datetime

api_key = config.API_KEY 
api_sec = config.API_SECRET
api_url = config.BASE_URL 
ticker_url = 'https://api.kraken.com/0/public/Ticker?pair=XDGUSD'

#Trades must operate by all of the following rules: 
##############################################################################
#
#    - If the overall market trend is bullish (upward trend)
#      - If the specific stock shows a consistent upward trend
#        - If the stock is performing better than its sector average
#          - If the stock's Price-to-Earnings (P/E) ratio is reasonable compared to historical averages
#            - If the company's earnings are growing consistently
#              - If the company has a strong balance sheet
#                - Then **Buy**
#              - Else
#                - Then **Hold**
#            - Else
#              - Then **Hold**
#          - Else
#            - Then **Hold or Re-evaluate**
#        - Else
#          - Then **Hold or Re-evaluate**
#      - Else
#        - Then **Hold or Re-evaluate**
#    - Else
#      - Then **Hold**

# 2. **If Market Trends are Unfavorable**
#    - If the overall market trend is bearish (downward trend)
#      - If the specific stock shows a consistent downward trend
#        - If the stock's Price-to-Earnings (P/E) ratio is high compared to historical averages
#          - If the company's earnings are declining
#            - If the company has a weak balance sheet
#              - Then **Sell**
#            - Else
#              - Then **Hold**
#          - Else
#            - Then **Hold or Re-evaluate**
#        - Else
#          - Then **Hold or Re-evaluate**
#      - Else
#        - Then **Hold or Re-evaluate**
#    - Else
#      - Then **Hold**

# 3. **If Market is Volatile**
#    - If the market shows high volatility (frequent large swings)
#      - If the stock is highly volatile
#        - If you have a low risk tolerance
#          - Then **Hold or Re-evaluate**
#        - Else
#          - If the stock has strong fundamentals
#            - Then **Hold**
#          - Else
#            - Then **Sell**
#      - Else
#        - Then **Hold**
#    - Else
#      - Then **Hold**

# 4. **If Market News or Events are Influential**
#    - If there are significant news events affecting the market or the specific stock (e.g., earnings reports, mergers, acquisitions)
#      - If news is positive
#        - If the stock price reacts positively
#          - If the positive news is likely to have a long-term impact
#            - Then **Buy**
#          - Else
#            - Then **Hold**
#        - Else
#          - Then **Hold**
#      - Else
#        - If news is negative
#          - If the stock price reacts negatively
#            - If the negative news is likely to have a long-term impact
#              - Then **Sell**
#            - Else
#              - Then **Hold**
#          - Else
#            - Then **Hold**
#    - Else
#      - Then **Hold**

# 5. **If Personal Financial Situation Changes**
#    - If your personal financial situation changes (e.g., need for liquidity, change in risk tolerance)
#      - If you need immediate liquidity
#        - Then **Sell**
#      - Else
#        - If your risk tolerance increases
#          - If market trends and stock fundamentals are favorable
#            - Then **Buy**
#          - Else
#            - Then **Hold**
#        - Else
#          - Then **Hold**

# 6. **If Technical Indicators are Relevant**
#    - If technical analysis supports the decision
#      - If moving averages show a golden cross (short-term MA crosses above long-term MA)
#        - Then **Buy**
#      - Else
#        - If moving averages show a death cross (short-term MA crosses below long-term MA)
#          - Then **Sell**
#        - Else
#          - Then **Hold**
#      - Else
#        - Then **Combine with other analyses and decide**
#
##############################################################################

def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key 
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

def is_bullish_trend(data):
    print("Running is_bullish_trend")

    # Calculate moving averages
    print(json.dumps(data, indent=4))
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    print(json.dumps(data, indent=4))

    # Calculate MACD
    data['MACD'] = ta.trend.MACD(data['Close']).macd()
    data['Signal'] = ta.trend.MACD(data['Close']).macd_signal()

    # Calculate RSI
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

    # Check Moving Averages crossover
    if data['MA50'].iloc[-1] > data['MA200'].iloc[-1]:
        ma_bullish = True
    else:
        ma_bullish = False

    # Check MACD crossover
    if data['MACD'].iloc[-1] > data['Signal'].iloc[-1]:
        macd_bullish = True
    else:
        macd_bullish = False

    # Check RSI
    if data['RSI'].iloc[-1] > 50:
        rsi_bullish = True
    else:
        rsi_bullish = False

    # Higher Highs and Higher Lows
    higher_highs_lows = (data['Close'].iloc[-1] > data['Close'].max()) and (data['Low'].iloc[-1] > data['Low'].min())

    # Determine overall trend
    if ma_bullish and macd_bullish and rsi_bullish and higher_highs_lows:
        return True  # Bullish Trend
    else:
        return False  # Not Bullish Trend

# Function to fetch Dogecoin price data from Kraken API
def fetch_dogecoin_data():
    try:
        # response = requests.get(api_url + "/0/public/Ticker?pair=DOGEUSD")
        response = requests.get(api_url + "/0/public/Ticker?pair=XDGUSD")
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        if 'error' in data and data['error']:
            raise Exception(data['error'])
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

#Fake Data just in case I need it
data = {
    "nonce": "1616492376594",
    "ordertype": "limit",
    "pair": "XBTUSD",
    "price": 37500,
    "type": "buy",
    "volume": 1.25
}
def fetch_data(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        if 'error' in data and data['error']:
            raise Exception(data['error'])
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Fetch the ticker data from Kraken API
ticker_data = fetch_data(ticker_url)

# start_date = datetime(2023,12,15)
# end_date = datetime(2023,12,31)

# signature = get_kraken_signature("/0/private/AddOrder", data, api_sec)
# print("API-Sign: {}".format(signature))

# Construct the request and print the result
print("Balance Info: ")
resp = kraken_request('/0/private/Balance', { "nonce": str(int(1000*time.time()))}, api_key, api_sec)
print(json.dumps(resp.json(), indent=4))

print("Doge Stats: ")
resp = fetch_dogecoin_data()
print(json.dumps(resp, indent=4))

print("Doge Advenced Stats: ")
if data:
    # Extract the last trade price for Dogecoin (XDG/USD)
    price = float(data['result']['XDGUSD']['c'][0])

    # Print the current price of Dogecoin
    print(f"The current price of Dogecoin is: ${price:.6f}")
else:
    print("Failed to fetch data from Kraken API.")

if ticker_data and 'result' in ticker_data and 'XDGUSD' in ticker_data['result']:
    try:
        price = float(ticker_data['result']['XDGUSD']['c'][0])
        print(f"The current price of Dogecoin is: ${price:.6f}")
    except (KeyError, ValueError, TypeError) as e:
        print(f"Failed to parse Dogecoin price data: {e}")
else:
    print("Failed to fetch Dogecoin price data from Kraken API.")

if balance_data and 'result' in balance_data:
    try:
        dogecoin_balance = balance_data['result'].get('XXDG', '0')
        usd_balance = balance_data['result'].get('ZUSD', '0')
        print(f"Dogecoin balance: {dogecoin_balance}")
        print(f"USD balance: {usd_balance}")
    except KeyError as e:
        print(f"Failed to parse balance data: {e}")
else:
    print("Failed to fetch balance data from Kraken API.")
# print(json.dumps(resp))gcc

# Check Doge as a a stock
#    - If the overall market trend is bullish (upward trend)
# et_grade = lambda score: "A" if score >= 90 else (
    # "B" if score >= 80 else (
        # "C" if score >= 70 else (
            # "D" if score >= 60 else "F"
        # )
    # )
# )
#    - If the specific stock shows a consistent upward trend
#    - If the stock is performing better than its sector average
#    - If the stock's Price-to-Earnings (P/E) ratio is reasonable compared to historical averages
#    - If the company's earnings are growing consistently
#    - If the company has a strong balance sheet

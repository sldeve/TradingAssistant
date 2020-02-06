import requests
import time
import hashlib
import hmac
from urllib.parse import urlparse
from position import Position
from exchange_data import get_bitmex


api_id = 'INSERT BITMEX ID HERE'
api_secret = 'INSERT BITMEX SECRET KEY HERE'

# Generates an API signature.
# A signature is HMAC_SHA256(secret, verb + path + expires + data), hex encoded.
# Verb must be uppercased, url is relative, expires must be unix timestamp (in seconds)
# and the data, if present, must be JSON without whitespace between keys.
def generate_signature(secret, verb, url, expires, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')

    print("Computing HMAC: %s" % verb + path + str(expires) + data)
    message = verb + path + str(expires) + data

    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    return signature

# fetch all position info from bitmex
def get_current_positions(secret, id_api):

    expires = int(round(time.time()) + 5000)
    sig = generate_signature(secret, 'GET', '/api/v1/position', expires, '')

    response = requests.get(
        'https://bitmex.com/api/v1/position',
        headers={'api-expires': str(expires), 'api-key': id_api, 'api-signature': sig},
    )
    positions = response.json()
    return positions

# return list of position objects that represent all OPEN positions 
def get_position_list(secret, id_api):
    position_data = get_current_positions(secret, id_api)
    position_list = []

    for positions in position_data:
        if positions['isOpen'] == True:
            pos = Position(positions['symbol'], positions['currentQty'], positions['markValue'], positions['avgEntryPrice'], 
            positions['markPrice'], positions['liquidationPrice'], positions['posMargin'], positions['leverage'], positions['unrealisedPnl'], positions['realisedPnl'])

            position_list.append(pos)
    return position_list

# return a concatenated string of all positions, each separated by new lines
def display_positions(secret, id_api):
    position_list = get_position_list(secret, id_api)
    position_string = ""
    total_unrealised_pnl = 0.0
    for pos in position_list:
        total_unrealised_pnl += float(pos.unrealised_pnl)
        position_string += str(pos) + "\n"
    position_string +="\nTotal Unrealised PNL: " + str(format(total_unrealised_pnl/100000000, 'f')) + " XBT"
    return position_string

#BALANCE FUNCTIONS

def balance_info(secret, id_api):
    expires = int(round(time.time()) + 5000)
    sig = generate_signature(secret, 'GET', '/api/v1/user/margin', expires, '')

    response = requests.get(
        'https://bitmex.com/api/v1/user/margin',
        headers={'api-expires': str(expires), 'api-key': id_api, 'api-signature': sig},
    )
    balance_data = response.json()
    return balance_data

def display_balance_info(secret, id_api):
    balance_data = balance_info(secret, id_api)
    balance_string = "Wallet Balance: " + str(format(balance_data['walletBalance'] / 100000000, 'f')) + " XBT" +" | $"+ str(round((balance_data['walletBalance']/100000000)*get_bitmex("xbtusd"), 2)) +"\n" + "Unrealised PNL: " + str(format(balance_data['unrealisedPnl'] / 100000000, 'f')) + " XBT" +" | $"+ str(round((balance_data['unrealisedPnl']/100000000)*get_bitmex("xbtusd"), 2)) +"\n"  + "Margin Balance: " + str(format(balance_data['marginBalance'] / 100000000, 'f')) + " XBT"" | $"+ str(round((balance_data['marginBalance']/100000000)*get_bitmex("xbtusd"), 2)) +"\n" + "Available Balance: " + str(format(balance_data['withdrawableMargin'] / 100000000, 'f')) + " XBT" " | $"+ str(round((balance_data['withdrawableMargin']/100000000)*get_bitmex("xbtusd"), 2)) +"\n" 
    return balance_string

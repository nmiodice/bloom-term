import http.client
import os
import json

API_ENDPOINT = 'query1.finance.yahoo.com'
API_PATH = '/v7/finance/quote'
API_FIELDS = ','.join([
    'symbol',
    'marketState',
    'regularMarketPrice',
    'regularMarketChange',
    'regularMarketChangePercent',
    'preMarketPrice',
    'preMarketChange',
    'preMarketChangePercent',
    'postMarketPrice',
    'postMarketChange',
    'postMarketChangePercent'
])

class format:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END_FORMAT = '\033[0m'


def format_string(fmt, msg):
    return '{0}{1}{2}'.format(fmt, msg, format.END_FORMAT)

def get(symbols, timeout):
    conn = http.client.HTTPSConnection(API_ENDPOINT, timeout = timeout)
    try:
        conn.request('GET', API_PATH + '?symbols=' + ','.join(symbols) + '&fields=' + API_FIELDS)
        response = conn.getresponse()
        if response.status != 200:
            print(format_string(format.RED, 'Cannot retrieve symbols... ' + response.reason))
            exit(-1)
    except:
        exit(-1)

    return json.loads(response.read().decode())

def format_line(symbol, price, percent, extra_info):
    # percent = percent * -1
    color = format.GREEN
    icon = '⬆️'
    if percent == 0:
        color = format.END_FORMAT
        icon = '〰️'
    if percent < 0:
        color = format.RED
        icon = '⬇️'

    trailing_text = ''
    if extra_info is not None and extra_info != '':
        trailing_text = '  ' + '({0})'.format(extra_info)

    return ''.join([
        icon.ljust(4),
        format_string(format.ORANGE, symbol),
        format_string(color, ' $' + str(price)),
        " (",
        format_string(color, "{:.2f}%".format(percent).ljust(5)),
        ")",
        trailing_text
    ])

def parse_single_result(result):
    symbol = result['symbol']

    if result['marketState'] == 'POST' and result['postMarketChange'] != None and result['postMarketChange'] != 0:
         return format_line(symbol, result['postMarketPrice'], result['postMarketChangePercent'], 'pst-mkt')

    if result['marketState'] == 'PRE' and result['preMarketChange'] != None and result['preMarketChange'] != 0:
         return format_line(symbol, result['preMarketPrice'], result['preMarketChangePercent'], 'pre-mkt')

    return format_line(symbol, result['regularMarketPrice'], result['regularMarketChangePercent'], '')

def print_results(response, display_per_line):
    results = [parse_single_result(r) for r in response['quoteResponse']['result']]

    if display_per_line < 0 or display_per_line >= len(results):
        print('   '.join(results))
        return

    max_len = 0
    for r in results:
        max_len = max(max_len, len(r))    
    results = [r.ljust(max_len) for r in results]

    lines = [results[i:i + display_per_line] for i in range(0, len(results), display_per_line)] 
    for line in lines:
        print('   '.join(line))
    

def run(symbols, display_per_line, timeout):
    symbols.sort()
    print_results(get(symbols, timeout), display_per_line)


if __name__ == '__main__':
    symbols = os.environ.get('BLOOM_TERM_SYMBOLS', None)
    if symbols is None:
        exit(0)
    
    display_per_line = int(os.environ.get('BLOOM_TERM_SHOW_PER_LINE', "-1"))
    timeout = float(os.environ.get('BLOOM_TERM_TIMEOUT', "1"))
    run([x.strip() for x in symbols.split(',')], display_per_line, timeout)
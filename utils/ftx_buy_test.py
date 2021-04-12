
x = {'bids': [[0.9415, 289.8], [0.941, 546.2], [0.939, 697.1], [0.9385, 5738.9], [0.938, 145.1]], 'asks': [[0.951, 7.6], [0.9515, 307.9], [0.957, 859.6], [0.9695, 388.5], [0.97, 5000.0]], 'timestamp': None, 'datetime': None, 'nonce': None}


import ccxt
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from decimal import Decimal

def round_down(number, precision):
    return decimal_to_precision(number_to_string(number), TRUNCATE, precision)


def book_oracle_buy(asset, book, precision, omega=0.8, max_rune=400):
    """ buy on book, sell on thorchain """
    book_rune_out_volume = []
    book_rune_out_price = []
    cap = False
    # [0] = price [1] = volume
    # Route 2: clearing ask side
    for i in range(0, 5):
        if cap:
            break
        omega_volume = float(round_down(book['asks'][i][1] * omega, precision))
        out_volume = max_rune if omega_volume > max_rune else omega_volume
        book_rune_out_volume.append(out_volume)
        book_rune_out_price.append(book['asks'][i][0])
        if i > 0:
            if book_rune_out_volume[i - 1] + book_rune_out_volume[i] >= max_rune:
                cap = True
                book_rune_out_volume[i] = max_rune
            else:
                book_rune_out_volume[i] += book_rune_out_volume[i - 1]
    return book_rune_out_volume, book_rune_out_price


# -*- coding: utf-8 -*-
import stock_utils
from stock_data_transformer import StockDataTransformer
from argparse import ArgumentParser
import os
import logging

TIMESTEP = 144
FUTURESTEP = 30
FEATURES = ['high', 'low', 'close']
OUT_DIR = 'out'


def main(args):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('s2i')
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    train_tickers, _ = stock_utils.get_sp500_tickers(limit=args.stocknum, ratio=.8)
    tickers_ohlcv_dict = stock_utils.get_ohlcv(train_tickers)
    transformer = StockDataTransformer(FEATURES, TIMESTEP, FUTURESTEP)
    for ticker in tickers_ohlcv_dict:
        ticker_data = tickers_ohlcv_dict.get(ticker)
        x, y = transformer.split_time_windows(ticker, ticker_data, balance=True, debug=False)


def read_args():
    parser = ArgumentParser(description='Predict future stock trend.')
    parser.add_argument('stocknum', type=int, help='number of sp500 stocks to retrieve (0=all)')
    parser.add_argument('epochs', type=int, help='number of training epochs')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='show visual information')

    return parser.parse_args()


if __name__ == '__main__':
    main(read_args())

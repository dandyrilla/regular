import pyupbit
import pandas as pd
from flask import Blueprint, redirect, url_for, request

from regular.util.fileio import json_load


bp = Blueprint('crypto', __name__, url_prefix='/crypto')


config = json_load('regular/config.json')
access_key = config['access_key']
secret_key = config['secret_key']
upbit = pyupbit.Upbit(access_key, secret_key)


def check_if_all_loaded(list1, list2):
    if not (sorted(list1) == sorted(list2)):
        n1, n2 = len(list1), len(list2)
        raise ValueError(f'Failed to load all tickers: {n2}/{n1}')


def get_balances(tickers=None):
    df = pd.DataFrame(upbit.get_balances())
    df = df.astype({'balance': float, 'avg_buy_price': float})
    df = df.rename(columns={'currency': 'ticker'})
    if tickers:
        df = df[df['ticker'].isin(tickers)]
        df = df.sort_values(
            by='ticker',
            key=lambda s: [tickers.index(ticker) for ticker in s],
        ).reset_index(drop=True)
        check_if_all_loaded(df['ticker'].tolist(), tickers)
    return df


def get_dummy_prices(fiat):
    return pd.DataFrame([{
        'ticker': fiat,
        'market': f'{fiat}-{fiat}',
        'price': 1.0,
    }])


def get_current_prices(markets):
    rows = []
    data = pyupbit.get_current_price(markets)
    if len(markets) == 1:
        market = markets[0]
        data = {market: data}
    for market, price in data.items():
        _, ticker = market.split('-')
        rows.append({
            'ticker': ticker,
            'market': market,
            'price': price,
        })
    df = pd.DataFrame(rows)
    check_if_all_loaded(df['market'].tolist(), markets)
    return df


@bp.route('/balances')
def show_balances():
    df = get_balances()
    return df.to_html()


@bp.route('/prices')
def show_prices():
    fiat = request.args.get('fiat', 'KRW')
    ticker = request.args.get('ticker')
    if ticker is None:
        default_ticker = 'BTC,ETH,XRP'
        return redirect(url_for(
            'crypto.show_prices',
            fiat=fiat,
            ticker=default_ticker,
        ))
    tickers = ticker.split(',')
    markets = [f'{fiat}-{ticker}' for ticker in tickers]
    try:
        df = get_current_prices(markets)
    except pyupbit.errors.UpbitError as e:
        return e.__str__()
    return df.to_html()


@bp.route('/')
def index():
    return 'crypto'

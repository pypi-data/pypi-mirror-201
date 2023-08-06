import requests
import datetime
import json
import os
import functools
import pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy

import boto3
import wallstreet as ws

from . import utils
from .cboe import CBOE
from .market import VolSurface, GEX, LiteBSOption
from . import market


def get_quote(ticker):
    key = json.load(open('credentials.json'))['td']['key']
    base_url = f'https://api.tdameritrade.com/v1/marketdata/{ticker.upper()}/quotes?'
    payload = {
        'apikey':key,
    }

    r = requests.get(base_url, params=payload)
    return r.json().get(ticker.upper())

@np.vectorize
@functools.lru_cache
def get_price(ticker, date=None):
    if date is None:
        quote = get_quote(ticker)
        return quote.get('regularMarketLastPrice')
    
    date = pd.to_datetime(date).date()
    t_minus_1 = date - datetime.timedelta(days=1)
    try:
        last_bar = get_bars(ticker, start_date=t_minus_1, end_date=date).iloc[-1]
    except KeyError:
        raise ValueError(f'No data for {date}')

    return last_bar.Close

def get_bars(ticker, n_days=1, start_date=None, end_date=None, frequency=5, frequency_type='minute', after_hours=False):
    key = json.load(open('credentials.json'))['td']['key']
    base_url = f'https://api.tdameritrade.com/v1/marketdata/{ticker.upper()}/pricehistory?'
    payload = {
        'apikey':key,
        'frequencyType':frequency_type,
        'frequency':frequency
    }
    
    epoch = datetime.datetime.utcfromtimestamp(0)
    if isinstance(n_days, int) and start_date is None and end_date is None:
        payload['periodType'] = 'day'
        payload['period'] = n_days
        end_date = datetime.datetime.today().replace(hour=23,minute=59,second=59)
        payload['endDate'] = int((end_date - epoch).total_seconds() * 1000)

    if isinstance(end_date, (str, pd.Timestamp, datetime.date, datetime.datetime)):
        end_date = pd.to_datetime(end_date).replace(hour=23,minute=59,second=59)
        payload['endDate'] = int((end_date - epoch).total_seconds() * 1000)

    if end_date is None:
        end_date = datetime.datetime.today().replace(hour=23,minute=59,second=59)
        payload['endDate'] = int((end_date - epoch).total_seconds() * 1000)

    if isinstance(start_date, (str, pd.Timestamp, datetime.date, datetime.datetime)):
        start_date = pd.to_datetime(start_date).replace(hour=0,minute=0,second=0)
        payload['startDate'] = int((start_date - epoch).total_seconds() * 1000)    
    
    r = requests.get(base_url, params=payload)
    data = r.json()

    df = pd.DataFrame(data['candles'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df.set_index('datetime', inplace=True)
    df.columns = map(str.capitalize, df.columns)
    if not after_hours:
        df = df.between_time('9:30', '15:59:59')
    
    return df

def get_historical_options(ticker,start_date=None,end_date=None):
    clean_ticker = ticker.replace('^','').upper()
    if clean_ticker not in ['SPY','SPX','BAC','QQQ','IWM','TSLA','JPM','AAPL','MSFT','NVDA']:
        raise ValueError('Only SPX and SPY are supported at this time')
    
    if clean_ticker == 'SPX':
        return get_historical_optionsOLD(clean_ticker)
    
    if start_date is None:
        start_date = 1
    else:
        start_date = pd.to_datetime(start_date).date()
        start_date = int(start_date.strftime('%Y%m%d'))

    if end_date is None:
        end_date = int(datetime.date.today().strftime('%Y%m%d'))
    else:
        end_date = pd.to_datetime(end_date).date()
        end_date = int(end_date.strftime('%Y%m%d'))

    creds = json.load(open('./credentials.json'))
    KEY = creds['aws']['key']
    SECRET = creds['aws']['secret']
    client = boto3.resource(
        'dynamodb',
        region_name='us-east-2',
        aws_access_key_id=KEY, 
        aws_secret_access_key=SECRET
        )
    table = client.Table('Options')

    items = []
    last_evaluated_key = None

    while True:
        query_params = {
            'KeyConditionExpression': 'ticker = :ticker and #date between :start_date and :end_date',
            'Limit': 100,
            'ExpressionAttributeValues': {
                ':ticker': ticker,
                ':start_date': start_date,
                ':end_date': end_date
            },
            'ExpressionAttributeNames': {
                '#date': 'date'
            }
        }
        if last_evaluated_key is not None:
            query_params['ExclusiveStartKey'] = last_evaluated_key
            
        r = table.query(**query_params)
        items.extend(r['Items'])
        last_evaluated_key = r.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break
    
    df = pd.concat([pd.read_pickle(pd.io.common.BytesIO(item.get('data').value)) for item in items])

    return df

def get_historical_optionsOLD(ticker):
    clean_ticker = ticker.replace('^','').upper()
    if clean_ticker not in ['SPY','SPX','BAC','QQQ','IWM','TSLA','JPM','AAPL','MSFT','NVDA']:
        raise ValueError('Only SPX and SPY are supported at this time')
    creds = json.load(open('./credentials.json'))
    user, token = creds.get('pythonanywhere').values()
    r = requests.get(
        f'https://www.pythonanywhere.com/api/v0/user/{user}/files/path/home/lwarner100/{clean_ticker}_options.pkl',
        headers={'Authorization': f'Token {token}'}
    )

    df = pd.read_pickle(pd.io.common.BytesIO(r.content))

    return df

class VolAnalysis:

    def __init__(self,ticker,historical=True,days=252):
        self.ticker = ticker
        self.vol_surface = VolSurface(ticker)
        self.gex = GEX(ticker)
        self.ws_obj = ws.Stock(ticker)
        self.vix = ws.Stock('^VIX')
        self.df = self.ws_obj.historical(days)
        self.df.set_index('Date',inplace=True)
        self.vix_df = self.vix.historical(days)
        self.vix_df.set_index('Date',inplace=True)
        self.df['vol20d'] = self.df.Close.pct_change().add(1).apply(np.log).rolling(20).std() * np.sqrt(252)
        self.df['vol10d'] = self.df.Close.pct_change().add(1).apply(np.log).rolling(10).std() * np.sqrt(252)
        
        if historical:
            self.options = get_historical_options(ticker)
        else:
            self.options = market.get_options(ticker)

    @staticmethod
    def bs_delta(s, k, t, r, sigma, contract_type):
        moneyness = s/k
        d1 = (np.log(moneyness.astype(float)) + (r + sigma**2/2)*t)/(sigma*np.sqrt(t))
        d = scipy.stats.norm.cdf(d1)
        if contract_type == 'P':
            d -= 1
        return d

    def get_implied_vol(self,x,expiration,type='P',date=None,x_var='delta'):
        valid_x_vars = ['delta','moneyness','strike','k']
        if x_var.lower() not in valid_x_vars:
            raise ValueError(f'`x_var` must be one of {valid_x_vars}')
        if date is None:
            date = utils.get_last_trading_day()
        else:
            date = pd.to_datetime(date).date()

        if isinstance(expiration, (datetime.date, datetime.datetime, pd.Timestamp)):
            expiration = pd.to_datetime(expiration).date()
            t = utils.date_to_t(expiration,t0=date)
        elif isinstance(expiration, str):
            if expiration[-1].isalpha():
                fracs = {
                    'd': 1/252,
                    'w': 1/52,
                    'm': 1/12,
                    'y': 1
                }
                freq = expiration[-1]
                n = int(expiration[:-1])
                t = n*fracs[freq]
            else:
                expiration = pd.to_datetime(expiration).date()
                t = utils.date_to_t(expiration,t0=date)
        elif isinstance(expiration, float):
            t = expiration

        # closest_expiration = self.options.expiration.iloc[(pd.to_datetime(expiration) - self.options.expiration).abs().argmin()]
        df = self.options.copy()
        if 'date' not in df.columns:
            df['date'] = datetime.date.today()
            df['date'] = df.date.astype('datetime64[ns]')
        df = df[((df.date-df.lastTradeDate).dt.days<3)&(df.date.dt.date==date)&(df.contractType==type)]
        df = pd.merge(df,self.df[['Close']],left_on='date',right_index=True,how='left')
        df['t'] = utils.date_to_t(df.expiration,t0=date)
        df['delta'] = self.bs_delta(
            s=df.Close,
            k=df.strike,
            t=df.t,
            sigma=df.impliedVolatility,
            r=0.04,
            contract_type=type
            )
        df = df[(df.delta.abs()<0.99)&(df.delta.abs()>0.01)].sort_values(['delta','t'])
        df['moneyness'] = df.Close/df.strike
        
        if x_var == 'delta':
            xs = df.delta.abs().values
        elif x_var == 'moneyness':
            xs = df.moneyness.values
        else:
            xs = df.strike.values
        
        ys = df.t.values
        zs = df.impliedVolatility.values
        f = lambda d, t,: scipy.interpolate.griddata((xs, ys), zs, (d,t), method='linear')
        # f = scipy.interpolate.interp1d(df.delta.abs(),df.impliedVolatility,kind='cubic')
        
        return f(x,t).item() if isinstance(x, float) and isinstance(t,float) else f(x,t)
    
    def dealer_gamma(self,date=None):
        if date is None:
            date = utils.get_last_trading_day()
        else:
            date = pd.to_datetime(date).date()

        df = self.options.copy()
        if 'date' not in df.columns:
            df['date'] = datetime.date.today()
        df = pd.merge(df,self.df[['Close']],left_on='date',right_index=True,how='inner')

        dealer_gammas = df.groupby('date').apply(lambda x: market.dealer_gamma(x, self.ticker, x.date.iloc[0]))

        return dealer_gammas

    def plot_iv(self,x,expiration,type='P',x_var='delta',realized=False):
        ivs = []
        dates = []
        for date in pd.DatetimeIndex(self.options.date.unique()).date:
            try:
                ivs.append(self.get_implied_vol(x,expiration,date=date,x_var=x_var,type=type))
                dates.append(date)
            except:
                pass
        
        fig, ax = plt.subplots(1,2,gridspec_kw={'width_ratios': [4, 1]},figsize=(10,4))
        
        ax[0].plot(dates,ivs,'-o',label='Implied Vol.')
        ax[0].set_title(f'{self.ticker} Implied Vol. | type = {type} | {expiration} | {x_var}={x}')
        ax[0].tick_params(axis='x', labelrotation=30)
        ax[0].text(dates[-1],ivs[-1]*1.015, f'{np.round(ivs[-1],3)}', ha='left', va='center', color='white', bbox=dict(facecolor='black', alpha=0.5))
        
        ax[1].set_yticks([])
        ax[1].set_xticks([])
        ax[1].hist(ivs,orientation='horizontal',density=True)
        ax[1].axhline(ivs[-1],color='black',linestyle='--')
        ax[1].set_title(f'%ile: {round(np.searchsorted(np.sort(ivs),ivs[-1])/len(ivs) * 100)}th')

        if realized:
            first_date = pd.DatetimeIndex(dates)[0].date()
            ax[0].plot(self.df[first_date:].index,self.df[first_date:].vol10d,label='Realized Vol. (10d)')
            ax[0].legend()

    def plot_dealer_gamma(self):
        gammas = self.dealer_gamma()
        gammas.plot()
        plt.title(f'{self.ticker} | Dealer Gamma')

class CBOEGEX:
    '''Object that retrieves the GEX data from the market'''
    
    def __init__(self, CLIENT_ID=None, CLIENT_SECRET=None):
        try:
            self.client = CBOE()
        except ValueError:
            self.client = CBOE(CLIENT_ID,CLIENT_SECRET)
        self.today = datetime.datetime.today()
        self.spy = ws.Stock('SPY')

    def get_gex(self,date=None):
        none_date = date is None
        if date:
            if isinstance(date,str):
                if 'e' in date:
                    date = self.client.convert_exp_shorthand(date)
                else:
                    date = pd.to_datetime(date)
            month = date.month
            year = date.year
            day = date.day or None
        else:
            month = self.today.month
            year = self.today.year
            day = None

        calls = self.client.get_options('SPY','C')
        puts = self.client.get_options('SPY','P')
        data = pd.concat([calls,puts])
        if not none_date:
            query = f'exp_month == {month} and exp_year == {year}' if not day else f'exp_month == {month} and exp_year == {year} and exp_day == {day}'
            data = data.query(query)

        return data.sort_values('strike')

    def plot(self, date=None, quantile=0.7):
        sequitur = 'for' if date else 'as of'
        if not date:
            str_date = self.today.strftime('%m-%d-%Y')
        elif 'e' in date:
            date = self.client.convert_exp_shorthand(date)
            str_date = date.strftime('%m-%d-%Y')
        else:
            date = pd.to_datetime(date)
            str_date = date.strftime('%m-%d-%Y')

        gex = self.get_gex(date)
        high_interest = gex[gex.agg_gamma > gex.agg_gamma.quantile(quantile)]

        aggs = {}
        underlying_price = self.spy.price
        spot = np.linspace(underlying_price*0.66,underlying_price*1.33,50)
        for i in high_interest.iterrows():
            i = i[1]
            option = LiteBSOption(
                s = underlying_price,
                k = i.strike,
                r = 0.04,
                t = i.expiry,
                sigma = i.mid_iv,
                type = i.option_type
            )
            gams = np.array([option.gamma(s=x)*i.open_interest*i.dealer_pos*100*underlying_price for x in spot])
            aggs.update({i.option:gams})

        agg_gammas = np.nansum(list(aggs.values()), axis=0)
        nearest_gamma = np.abs(spot - underlying_price).argmin()
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(spot, agg_gammas, label='Dealer Gamma')
        ax.set_xlim(spot[0],spot[-1])
        ax.vlines(underlying_price,0,agg_gammas[nearest_gamma],linestyle='--',color='gray')
        ax.hlines(agg_gammas[nearest_gamma],spot[0],underlying_price,linestyle='--',color='gray')
        ax.plot(underlying_price, agg_gammas[nearest_gamma], 'o', color='black', label='Spot')
        ax.set_title(f'Dealer Gamma Exposure {sequitur} {str_date}')
        ax.set_xlabel('Strike')
        ax.set_ylabel('Gamma Exposure')
        ax.axhline(0,color='black')
        # add text saying the spot price in black text with white outline to the right of the point
        ax.text(underlying_price*1.02, agg_gammas[nearest_gamma], f'${underlying_price:,.2f}', ha='left', va='center', color='white', bbox=dict(facecolor='black', alpha=0.5))
        ax.legend()
        ax.grid()
        plt.show()

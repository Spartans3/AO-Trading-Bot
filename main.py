import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
from binance.client import Client
from api_keys import binance_api_key, secret_key

client = Client(binance_api_key,secret_key)



def getMinuteData(symbol, interval, lookback, UTC):
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval, lookback + ' min ago UTC' +UTC))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

print(getMinuteData('DOGEUSDT', '1m', '30', '+0'))

test = getMinuteData('DOGEUSDT', '1m', '30', '+0')

client.hisrec

plt.figure()
plt.plot(test)
plt.show()

#buy if asset fell by more then 0.2% within the last 30 min
#sell if asset rises by more then 0.15% or falls further by 0.15%

def strategyTest(symbol, quantity, entried=False):
    df = getMinuteData(symbol, '1m', '30', '')
    cumulret = (df.pct_change() +1).cumprod() -1
    if not entried:
        if cumulret[-1] < -0.002:
            order = client.create_order(symbol = symbol, side='BUY', type='MARKET',)


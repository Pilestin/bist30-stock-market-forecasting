import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as date
from matplotlib.pylab import rcParams

import yfinance as yf



from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler

rcParams['figure.figsize']=20,10




today = date.today().strftime('%Y-%m-%d')
# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.
df = yf.download("XU030.IS", 
                start="2020-09-22", 
                end=today)
                 

print(df)


"""
df["Date"] = pd.to_datetime(df.index,format="%Y-%m-%d"!)
print(df)

df.index=df['Date']
print(df)
"""
plt.figure(figsize=(16,8))
plt.plot(df["Close"],label='Close Price history')
plt.show()
"""
data=df.sort_index(ascending=True,axis=0)
new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close']) 

for i in range(0,len(data)):
    new_dataset["Date"][i]=data['Date'][i]
    new_dataset["Close"][i]=data["Close"][i]

"""
import numpy as np
from datetime import datetime as date
from ta.momentum import RSIIndicator
import yfinance as yf

today = date.today().strftime('%Y-%m-%d')
# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.
df = yf.download("XU030.IS", 
                 start="2020-09-22", 
                 end=today)
                 
print(df)           

print(df.info())

indicatorRsi = RSIIndicator(close=df["Close"], window = 10, fillna = False )
df["rsi"] = indicatorRsi.rsi()
numpyType = df.values

print(df)
cor_mat = np.corrcoef(numpyType.T)
# print ("Correlation matrisinin sekli:", cor_mat.shape)
print(df.tail(30))

# sns.heatmap(cor_mat, 
#     xticklabels=df.columns, 
#     yticklabels=df.columns)
# plt.show()
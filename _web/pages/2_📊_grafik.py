import streamlit as st 
from PIL import Image
import numpy as np
from datetime import datetime as date
import yfinance as yf


st.set_page_config(layout="wide")



kod = {"BIST30":"XU030.IS", "BIST100":"XU100.IS", "Türk Hava Yollari":"THYAO.IS" }
# XU100.IS 
# THYAO.IS

option = st.selectbox(
    'Seçiminiz',
    ('BIST30', 'BIST100','Türk Hava Yollari'))

col1 , col2 = st.columns(2)
col1.write('You selected:', option)
col2.write("borsa : ",kod[option])



st.write('You selected:', option)
st.write(type(option))

st.write("borsa : ",kod[option])
st.write("tip : ", type(kod[option]))


today = date.today().strftime('%Y-%m-%d')
# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.
df = yf.download("XU030.IS", 
                start="2020-09-22", 
                end=today)
                 



st.write(df)
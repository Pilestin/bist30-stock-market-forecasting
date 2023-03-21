import streamlit as st 
import streamlit.components.v1 as components
from datetime import datetime as date
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide" ,page_icon=':chart')



kod = {"BIST30":"XU030.IS", "BIST100":"XU100.IS", "Türk Hava Yollari":"THYAO.IS" }
# XU100.IS 
# THYAO.IS

from data.container import getBistInfo

bist30 = getBistInfo()

option = st.selectbox(
    'Lütfen hisse seçin : ',
    tuple(bist30.keys()))

option = st.selectbox(
    'Lütfen endeks seçin : ',
    ("BIST100","BIST30"))

col1 , col2 = st.columns(2)

with col1:
    st.header("İsmi")
    components.html("<hr>" + option)


with col2:
    st.header("Kodu")
    components.html("<hr>" + kod[option])
   
    


today = date.today().strftime('%Y-%m-%d')
# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.
df = yf.download(kod[option], 
                start="2020-09-22", 
                end=today)



with st.container():
    st.write(df)

st.dataframe(data=df.style.highlight_max(axis=0),use_container_width=True, height=500)



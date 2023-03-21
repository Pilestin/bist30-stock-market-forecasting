import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

import streamlit as st 
import streamlit.components.v1 as component

from datetime import datetime as date
import yfinance as yf
from data.container import getBistInfo



st.set_page_config(page_title='Bitirme Projesi', page_icon=':house', layout='wide')
component.iframe("https://apption.co/embeds/0f75bf4d")

st.title('Makine Öğrenmesi ile Bist30 Borsa Fiyat Tahmini')
    

st.write("---")

data_sets  = getBistInfo()


option = st.selectbox(
    'Lütfen hisse seçin : ',
    tuple(data_sets.keys()))


col1,col2 = st.columns(2)

today = date.today().strftime('%Y-%m-%d')       # ["2023","3","20"] 
today = [int(i) for i in today.split("-")]     # [2023, 3 , 20]
                           

with col1:
    begin_time = st.date_input(
    "Başlangıç tarihi seçin :",
    date(2020, 9, 22))
    
with col2:
    end_time = st.date_input(
    "Bitiş tarihi seçin :",
    date(today[0],today[1],today[2]))

# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.s

df = yf.download(data_sets[option], 
                start=str(begin_time),
                end=str(end_time))

tab1, tab2,tab3 = st.tabs(["Hisse Hakkında","Veriler", "Grafik"])

with tab1:
    st.header(option)
    

with tab2:
    st.dataframe(data=df.style.highlight_max(axis=0),use_container_width=True, height=500)

with tab3:
    st.line_chart(data=df[["Close","Open"]],  use_container_width=True)
    
    d1 = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

    d2 = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['d', 'e', 'f'])

    st.line_chart(d1)
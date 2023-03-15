import streamlit as st 
from PIL import Image
import numpy as np
from datetime import datetime as date
import yfinance as yf


st.set_page_config(layout="wide")


option = st.selectbox()

kod = {}
# XU100.IS 
# THYAO.IS
today = date.today().strftime('%Y-%m-%d')
# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.
df = yf.download("XU030.IS", 
                start="2020-09-22", 
                end=today)
                 

st.write(df)
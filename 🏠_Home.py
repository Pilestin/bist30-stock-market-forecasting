import plotly.graph_objects as go
import matplotlib.pyplot as plt
# -------------------------------------
import streamlit as st
import streamlit.components.v1 as component
import pandas as pd
import numpy as np
# -------------------------------------
from datetime import datetime as date
import time
import calendar
# -------------------------------------
from data.get_names import getBistInfo
from data.BistIndicators import BistIndicators
from data.CurrentData import CurrentData
from models.lineer_regression import model_lineer_regression
from models.neural_network import model_neural_network
from models.lstm import model_lstm
# -------------------------------------
from sklearn.preprocessing import MinMaxScaler 
from sklearn.model_selection import train_test_split 
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


st.set_page_config(page_title='Bitirme Projesi',
                   page_icon=':house', layout='wide')


st.title('Makine Öğrenmesi ile Borsa Fiyat Tahmini')

st.write("---")

# getBistInfo bir dictionary yapısı döndürür.
# ?
#   Key değerleri    : BİST hisse adları
#   Values değerleri : BİST hisse kodları

bist_dict = getBistInfo()

hisse_adi = st.selectbox(
    'Lütfen hisse seçin : ',
    tuple(bist_dict.keys()))


today = date.today().strftime('%Y-%m-%d')       # ["2023","3","20"]
today = [int(i) for i in today.split("-")]      # [2023, 3 , 20]


with open("./css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


col_beginTime, col_endTime = st.columns(2)
with col_beginTime:

    try:
        begin_time = st.date_input("Başlangıç tarihi seçin :", date(2020, 7, 27))
        
    except:
        st.error("Bir başlangıç ve bitiş tarihi seçmelisiniz.")
        st.stop()

with col_endTime:
    try:
        end_time = st.date_input("Bitiş tarihi seçin :", date(today[0], today[1], today[2]))
        
    except:
        st.error("Bir başlangıç ve bitiş tarihi seçmelisiniz.")
        st.stop()

if begin_time > date.now().date() or end_time > date.now().date():
    st.error(
        "Başlangıç tarihi veya Bitiş tarihi bugünün tarihinden büyük olamaz.")
    st.stop()

elif begin_time > end_time:
    st.error("Başlangıç tarihi Bitiş tarihinden büyük olamaz.")
    st.stop()

# Bugün dahil olmadığı için +1 ekliyoruz.
# ----------------------------------------
end_time = [int(i) for i in str(end_time).split("-")] 
year, month, day = end_time
last_day = calendar.monthrange(year, month)[1] 
if day == last_day and end_time[1] == 12:
    end_time[0] = end_time[0] + 1
    end_time[1] = 1
    end_time[2] = 1
elif day == last_day:
    end_time[1] = end_time[1] + 1
    end_time[2] = 1
else:
    end_time[2] = end_time[2] + 1
# ----------------------------------------
_end_time = date(end_time[0], end_time[1], end_time[2])
# datetime.datetime to datetime.date 
# 2023-05-17 00:00:00 -> 2023-05-17 haline getiriyoruz.
end_time = _end_time.date() 


# Burada yahoo finans kullanarak BİST30 -> XU030.IS verilerini inceleyebileceğiz. Herhangi ekstra dosya olmadan verileri alacağız.s
data_frame = CurrentData(begin_time=begin_time, end_time=end_time,
                         bist_dict=bist_dict, choosen=hisse_adi).df

data_frame = data_frame[::-1]

st.session_state["data_frame"] = data_frame

# BURAYI CurrentData SINIFINA TAŞIDIM
# Eğer son günün hacmi 0 ise, son 10 günün ortalamasını alıyoruz. 
# if data_frame.loc[data_frame.index[-1], 'Volume'] == 0:
    
#     son_10 = data_frame.tail(10) 
#     ortalama_son_10 = son_10["Volume"].mean()
#     data_frame.loc[data_frame.index[-1], 'Volume'] = ortalama_son_10


indicator_obj = BistIndicators(st.session_state.data_frame[::-1])
indicators = indicator_obj.indicators  # dictionary döndürür.

col_select_model, col_select_indicators = st.columns(2)

with col_select_model:
    selected_model = st.selectbox(
        'Tahmin için makine öğrenimi yöntemini seçiniz :',
        ('Lineer Regresyon', 'Yapay Sinir Ağları', 'LSTM'))   
            

with col_select_indicators:
    selected_indictors = st.multiselect(
        'Teknik göstergeleri ekleyiniz :',
        indicators.keys(),  # dictionary'nin key'lerini döndürür.(RSI, MACD, ...)
        help="Modelin eğitilmesine kullanılmasını istediğiniz teknik göstergeleri seçebilirsiniz.\n 1",
        
    )
    #selected_indictors = ["RSI", "CMF", "Aroon", "Stoch", "CCI", "MFI", "KC", "WILL", "EOM", "MASS"]
    with st.spinner("Veriler yükleniyor..."):
        time.sleep(1)
    

st.session_state.data_frame = indicator_obj.set_indicators(st.session_state.data_frame, selected_indictors)


tab_veriler, tab_grafik, tab_model, tab_tahmin_grafik = st.tabs(
    [ "Veriler", "Grafik", "Model", "Tahmin Grafiği"])

with st.container():
    
    
    with tab_veriler:
        
        st.write(st.session_state.data_frame.shape)
        st.dataframe(st.session_state.data_frame, use_container_width=True)
        st.dataframe(st.session_state.data_frame.describe(), use_container_width=True )
        st.subheader("X verileri")
        st.dataframe(data_frame.drop( axis=1, columns=["Adj Close", "Close"]), use_container_width=True)
        st.subheader("Y verileri")
        st.dataframe( data_frame[["Close"]], use_container_width=True)
        # X_1  = st.session_state.data_frame.drop( axis=1, columns=["Adj Close", "Close"])
        # Y_1  = st.session_state.data_frame[["Close"]]
        
        # X_2 = st.session_state.data_frame.drop( axis=1, columns=["Adj Close"])
        # Y_2 = st.session_state.data_frame[["Close"]].shift(+1)

        
    
    with tab_grafik:
            
        fig = go.Figure(data=[go.Candlestick(x=data_frame.index,
                                            open=data_frame['Open'],
                                            high=data_frame['High'],
                                            low=data_frame['Low'],
                                            close=data_frame['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)

        
        candle = st.checkbox('Mum Grafiği Göster')
        agree = st.checkbox('Teknik Göstergeleri Göster')

        if candle:
            st.plotly_chart(fig, use_container_width=True)

        element = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)

        if agree:
            st.write("Teknik göstergeleri gösteriliyor.")
            df = st.session_state.data_frame
            # element = st.line_chart()
            
            digerleri = []
            for col_name in st.session_state.features:
                
                if col_name == "Open" or col_name == "High" or col_name == "Low" or col_name == "Volume":
                    continue
                else: 
                    st.write(col_name)
                    digerleri.append(col_name)
            
            element.add_rows(df[digerleri])
        
        # """ 
        # correlation_matrix = data_frame.corr()
        # st.write(correlation_matrix)
        # st.write("Burası tam olmadı")
        # fig, ax = plt.subplots(sharey=True, sharex=True) 
        # sns.heatmap(correlation_matrix)
        # st.write(fig)


        # fig_cor = plt.subplots() 
        # sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
        # plt.title("Korelasyon Matrisi")
        # st.pyplot(fig_cor) 
        # """   

    with tab_model:
        
        # özellikleri features listesinde tutalım
        features = ['Open', 'High', 'Low', 'Volume']
        for ind in selected_indictors:
                features.append(ind)
        # ve session olarak ekleyelim
        st.session_state['features'] = features
        
        # Son gündeki gerçek kapanış verisini session'a ekleyelim => target
        
        gercek =  float(st.session_state.data_frame[0:1]["Close"].values[0])
        st.session_state['target'] = gercek

        last_row = st.session_state.data_frame.iloc[0:1]
        last_day = last_row.index[0]
        

        
    # MODEL EĞİTİMİ 
    # -------------------------------------
        model =  None
        if selected_model == "Lineer Regresyon":

            st.write("Lineer Regresyon seçildi")
            
            # tahmin : son Close değerinin tahmini
            # predictions : x_Test verilerinin tahmin somnuçları 
            model_lineer, tahmin, predictions, rmse, r2, mae = model_lineer_regression(st.session_state.data_frame, st.session_state.features)
            
            gercek = st.session_state.target
            
            st.session_state["predictions"] = predictions
            st.session_state["r2_score"] = r2
            st.session_state["rmse"] = rmse
            st.session_state["mae"] = mae
            
            model = model_lineer
            
        elif selected_model == "Yapay Sinir Ağları":
            
            st.write("Yapay Sinir Ağları seçildi")
            # deneme
            # tahmin : son Close değerinin tahmini
            # predictions : x_Test verilerinin tahmin somnuçları 
            model_nn, tahmin, predictions, rmse_nn, r2_score_nn, scaler_X, scaler_y = model_neural_network(st.session_state.data_frame)
            
            gercek = st.session_state.target
            mae = mean_absolute_error(predictions["Original"], predictions["Predicted"])
            
            st.session_state["predictions"] = predictions
            st.session_state["rmse"] = rmse_nn
            st.session_state["r2_score"] = r2_score_nn
            st.session_state["mae"] = mae

        
            model = model_nn
        
        elif selected_model == "LSTM":
            
            st.write("LSTM seçildi")
            
            # model_ls, tahmin, predictions, rmse_ls, r2_score_ls = model_lstm(st.session_state.data_frame)
            # gercek = st.session_state.t
            # st.session_state["predictions"] = predictions
            # st.session_state["rmse"] = rmse_ls
            # st.session_state["r2_score"] = r2_score_ls
                
            # fiyat_farki = tahmin - gercek
            # mutlak_fark = abs(fiyat_farki)
            # yuzde_fark  = (mutlak_fark/gercek) * 100
            
            data_frame = data_frame[::-1]
            dates = data_frame.index

            Y = data_frame["Close"]
            X = data_frame.drop(columns=["Close","Adj Close"], axis=1)
            
            # Verileri normalize etme
            scaler_X = MinMaxScaler()
            scaler_y = MinMaxScaler()
            X_ = scaler_X.fit_transform(X)
            Y_ = scaler_y.fit_transform(Y.values.reshape(-1, 1)) # 2 boyutlu array'e çeviriyoruz.  

            # normalized data to dataframe
            X_ = pd.DataFrame(X_, columns=X.columns )
            # set X column name : Open, High, Low, Volume : 
            Y_ = pd.DataFrame(Y_, columns=["Close"])

            X_.index = dates 
            Y_.index = dates
            
            last_X = X_.iloc[-1:]
            last_Y = Y_.iloc[-1:]

            X_ = X_.drop(last_X.index) 
            Y_ = Y_.drop(last_X.index) 
        
            X_train, X_test, y_train, y_test = train_test_split(X_, Y_, train_size= 0.8, shuffle=False)
            
            # --------------------------------------------
            # MODELİ EĞİTME
            model = Sequential()
            model.add(LSTM(units=40, return_sequences=True, input_shape=(1, X_train.shape[1])))
            model.add(LSTM(units=40))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer="adam", metrics=['accuracy'])
            model.fit(X_train.values.reshape(X_train.shape[0], 1, X_train.shape[1]), y_train, epochs= 20, batch_size= 8, validation_data=(X_test.values.reshape(X_test.shape[0], 1, X_test.shape[1]),  y_test))
            
            predictions = model.predict(X_test.values.reshape(X_test.shape[0], 1, X_test.shape[1]))                     # sonuçlar alındı
            predictions = scaler_y.inverse_transform(predictions)   # normalize edilmiş veriler gerçek verilere çevrildi
            predictions = pd.DataFrame(predictions, columns=['Predicted'])  # dataframe'e çevrildi
            predictions["Original"] = scaler_y.inverse_transform(y_test.values)                  # gerçek veriler eklendi
            # date 
            predictions.index = y_test.index                    
            # last_X = last_X.values.reshape(last_X.values.shape[0], 1, last_X.values.shape[1])
            # _tahmin = model.predict(last_X)
            
            _tahmin = model.predict(last_X.values.reshape(last_X.shape[0], 1, last_X.shape[1]))
            
            
            tahmin = float(scaler_y.inverse_transform(_tahmin))
            gercek_mi = scaler_y.inverse_transform(last_Y.values)
            
            # --------------------------------------------
            r2_score_ls = r2_score(predictions["Original"], predictions["Predicted"])
            rmse_ls = np.sqrt(np.mean((predictions["Original"] - predictions["Predicted"]) ** 2))
            mae = mean_absolute_error(predictions["Original"], predictions["Predicted"])
        
            st.session_state["predictions"] = predictions
            st.session_state["rmse"] = rmse_ls
            st.session_state["r2_score"] = r2_score_ls
            st.session_state["mae"] = mae
            
            
         
                
        with open("./css/style.css") as source:
            style = source.read()
          
        fiyat_farki = tahmin - gercek
        mutlak_fark = abs(fiyat_farki)
        yuzde_fark  = (mutlak_fark/gercek) * 100  
          
        # FARKLAR VE FİYAT             
        with st.container():
            column_fark, column_fiyat = st.columns(2)
            # Aradaki fark paneli
            with column_fark:
                if (mutlak_fark >= 100):
                    
                    message = "Kötü tahmin"
                    st.metric("Aradaki fark", f"{float(fiyat_farki):.4f} ₺", message)
                    st.metric("yüzdelik fark : ", f"%{float(yuzde_fark):.3f}")
                    color = "#ffb980" # turuncu
                elif (mutlak_fark < 100 and mutlak_fark >= 50):
                
                    message = "Ortalama tahmin"
                    st.metric("Aradaki fark", f"{float(fiyat_farki):.4f} ₺", message)
                    st.metric("yüzdelik fark : ", f"%{float(yuzde_fark):.3f}")
                    color = "#fbff80"  # sarı-yeşil
                    
                elif (mutlak_fark < 50 and mutlak_fark >= 20):
                    
                    message = "İyi tahmin"
                    st.metric("Aradaki fark", f"{float(fiyat_farki):.4f} ₺", message)
                    st.metric("yüzdelik fark : ", f"%{float(yuzde_fark):.3f}",)
                    color = "#d4f792"  # yeşil
                elif (mutlak_fark < 20 and mutlak_fark >= 0):
                    
                    message = "Mükemmel tahmin"
                    st.metric("Aradaki fark", f"{float(fiyat_farki):.4f} ₺", message)
                    st.metric("yüzdelik fark : ", f"%{float(yuzde_fark):.3f}",)
                    color = "#28fa02"  # en-yeşil 
                        
        
            
            # Fiyatların renkli gösterimi
            with column_fiyat:
                gercek = st.session_state.target
                component.html(f"""
                <style>
                    {style}
                </style>
                <div class="kapanis-fiyati">
                    <h3 style="margin:15px;">
                        {str(last_day).split()[0]} Kapanış fiyatı : <span class="gercek-fiyat"> {gercek}₺ </span>
                    </h3>
                </div>
                    </br>
                <div class="model-tahmin-fiyati" style="background-color: {color}">
                    <h3 style="margin:15px;">
                        Model tahmini :   <span class="tahmin-fiyat"> {tahmin}₺ </span>
                    </h3>               
                </div>         
                    """, height=300 )    
        
        
        # METRİKLER BÖLÜMÜ 
        with st.container():
            metric_1, metric_2, metric_3 = st.columns(3)
            with metric_1:
                st.metric("R2 Performansı", st.session_state.r2_score)
            with metric_2:
                st.metric("RMSE Performansı", float(st.session_state.rmse ))
            with metric_3:
                st.metric("MAE Performansı", float(st.session_state.mae ))    
        st.write("------")   
        
        # TAHMİN SONUÇLARI pandas olan BÖLÜMÜ
        with st.container():  
            st.dataframe(st.session_state.predictions   , use_container_width=True)
        
        # GRAFİK BÖLÜMÜ
        with st.container():
            grafic = st.line_chart(data_frame[["Close"]])    
            predictions["Predicted"] = predictions["Predicted"].astype("float64")
            grafic.add_rows(predictions[["Original"]])
            grafic.add_rows(predictions[["Predicted"]])
            
        st.write("-----")

        # MODELİ EL İLE TEST ETME BÖLÜMÜ
        with st.container():
            st.subheader("Modeli Verilen Değerler ile Test Etme")
            col_1, col_2, col_3, col_4 = st.columns(4)

            with col_1:
                open = st.number_input("Open", value=last_row["Open"].values[0])
                st.write(open)

            with col_2:
                high = st.number_input("High", value=last_row["High"].values[0])
                st.write(high)

            with col_3:
                low = st.number_input("Low", value=last_row["Low"].values[0])
                st.write(low)

            with col_4:
                vol = st.number_input("Volume", value=last_row["Volume"].values[0])
                st.write(vol)
        
        
            last_row["Open"] = open 
            last_row["High"] = high
            last_row["Low"] = low
            last_row["Volume"] = vol
            last_row = last_row.drop(axis=1, columns=["Adj Close", "Close"])
            
            
            
            # SON GÜN VE BUTON BÖLÜMÜ
            col1, col2 = st.columns(2)
            with col1:
                st.write(last_row)
            with col2:
                st.write("")
                buton = st.button("Çalıştır", use_container_width=True)
            
            result = "Sonucu görmek için butona tıklayın"
            
            if selected_model == "LSTM" and buton:
                last_row = scaler_X.transform(last_row)
                result = model.predict(last_row.reshape(last_row.shape[0], 1, last_row.shape[1]))
                result = float(scaler_y.inverse_transform(result))
            
            elif selected_model == "Yapay Sinir Ağları" and buton:
                last_row = scaler_X.transform(last_row)
                result = model.predict(last_row)
                result = float(scaler_y.inverse_transform(result))
                
            elif selected_model == "Lineer Regresyon" and buton:
                result = float(model.predict(last_row))

        component.html(f"""
            <h3 style="background-color:#06AAD6; padding:15px; color:white; border-radius:10px ">
            Verdiğiniz değerlere göre kapanış fiyatı :  
            <span style="color:black; font-size:150%; text-align:center;" > 
            {result}
                </span>
            
            </h3>
            """)

        st.write("Bu son kısımda verilere sanırım indikatörler eklenmedi!")

    with tab_tahmin_grafik:
        st.subheader("Tahmin Değerleri ve Grafiği")
        # st.write("Bu kısımda tahmin grafiği olacak.")
        # element = st.line_chart(data=st.session_state.predictions[["Original"]],  use_container_width=True)
        # element.add_rows(st.session_state.predictions[["Predicted"]] )
        # st.dataframe(st.session_state.predictions, use_container_width=True)



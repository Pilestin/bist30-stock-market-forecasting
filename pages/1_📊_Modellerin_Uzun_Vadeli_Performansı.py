import streamlit as st
import streamlit.components.v1 as component
from models.lineer_regression import *
from models.lstm import *
from models.neural_network import *
from data.BistIndicators import *
from data.get_names import *
from datetime import date
import yfinance as yf
import pandas as pd
import time
from keras.models import load_model
from sklearn.metrics import  mean_squared_error, mean_absolute_error
import numpy as np



st.set_page_config(page_title='Grafik',
                   page_icon='', layout='wide')

def getData(hisse, start, end):
    data = yf.download(hisse, start=start, end=end)
    return data


bist_dict = getBistInfo()

hisse_adi = st.selectbox(
    'Lütfen hisse seçin : ',
    tuple(bist_dict.keys()))

t_begin = st.sidebar.date_input('Başlangıç Tarihi', date(2020, 7, 27))
t_end = st.sidebar.date_input('Bitiş Tarihi(+1 ekleyiniz)', date(2023, 4, 5)) # 2023-04-04 seçilir

today_str = date.today().strftime('%Y-%m-%d')       # ["2023","3","20"]
today_int = [int(i) for i in today_str.split("-")]      # [2023, 3 , 20]
today_date = date(today_int[0], today_int[1], today_int[2])
# son gün için bugünü verirsek düne kadar olanı alır. Bir fazla vermen lazım 
tomorrow = date(today_int[0], today_int[1], today_int[2]+1)

# tabta seçilen tarihi bir gün geri alıyoruz.
t_end_day = t_end.strftime('%Y-%m-%d')       # ["2023","3","20"]
t_end_int = [int(i) for i in t_end_day.split("-")]      # [2023, 3 , 20] 
t_end_real = date(t_end_int[0], t_end_int[1], t_end_int[2]-1)


data_frame = getData(bist_dict[hisse_adi],t_begin, t_end)
test_data = getData(bist_dict[hisse_adi], t_end_real, tomorrow).drop( columns=["Adj Close"], axis=1)
test_data = test_data[::-1]


if test_data.loc[test_data.index[0], 'Volume'] == 0:
    son_10 = test_data.head(10) 
    ortalama_son_10 = son_10["Volume"].mean()
    test_data.loc[test_data.index[0], 'Volume'] = ortalama_son_10

indicator_obj = BistIndicators(data_frame)
indicators = indicator_obj.indicators  # dictionary döndürür.

new_ind = BistIndicators(test_data)




col_model , col_indicator = st.columns(2)
with col_model:
    
    secilen_model = st.selectbox('Model seç :', ('Lineer Regresyon', 'Yapay Sinir Ağları', 'LSTM')) 
     
with col_indicator:
    
    selected_indictors = st.multiselect(
        'Teknik göstergeleri ekleyiniz :',
        indicators.keys(),  # dictionary'nin key'lerini döndürür.(RSI, MACD, ...)
        help="Modelin eğitilmesine kullanılmasını istediğiniz teknik göstergeleri seçebilirsiniz.",
        
    )
    with st.spinner("Veriler yükleniyor..."):
        time.sleep(1)
        
data_frame = indicator_obj.set_indicators(data_frame[::-1], selected_indictors)
test_data = new_ind.set_indicators(test_data, selected_indictors)
# SON GÜNÜ AYIRMA
last_test = test_data.iloc[0:1:]
target = test_data["Close"].shift(+1)



col_testData, col_target = st.columns(2)
with col_testData:
    st.subheader("X - girdi verisi")
    st.write(test_data)
    st.write(f"{test_data.index[0]} günü çıkarılacak ve ayrıca test edilecektir.")
    st.write("test_data shape : ", test_data.shape)

with col_target:
    
    col_y, col_acıklama = st.columns(2)
    target = target.dropna()
    
    with col_y:
        st.subheader("Y - hedef verisi")
        st.write(target,use_container_width=True)
        
    with col_acıklama:
        
        st.subheader("Not :")
        st.write("Y - hedef verisi, X - girdi verisinden bir gün sonraki Close değerini alır.")
        st.write("Böylece verilen gün satırına karşılık, sonraki günün çıktısını bulabiliriz.")
        
        st.subheader("Not 2 :")
        st.write(f"{test_data.index[0]} tarihli veriye karşılık Y değeri bulunamadığı için çıkarılmıştır.") 




if secilen_model == 'Lineer Regresyon':
    
    model, predictions, rmse, r2 = model_lineer_regression_2(data_frame)
    
    
    # LİNEER REGRESYON İÇİN PREDİCT
    # ----------------------------- 
    
elif secilen_model == 'Yapay Sinir Ağları':
    
    model, score, scaler_X, scaler_y = model_neural_network_2(data_frame)
    model = load_model('model_saves/nn_model2.h5')
    st.write(f"{model.metrics_names[0]} : {float(score[0])}")
    st.write(f"{model.metrics_names[1]} : {float(score[1])}")

elif secilen_model == 'LSTM':
    
    model, rmse, r2, scaler_y, scaler_X = model_lstm_2(data_frame)
    model = load_model('model_saves/lstm_model_60.h5')
    # normalize_veri = model.predict(dun_x.values.reshape(dun_x.shape[0], dun_x.shape[1], 1))
    # # LSTM İÇİN PREDİCT
    # # -----------------------------
    # bugun_tahmin = reverse_data_y(normalize_veri, scaler_y)



test_data = test_data.drop(index=[test_data.index[0]], axis=0)
# Ek tarih çerçevesi, günler kaydırılmıştır.
# Sonuç çerçevesine eklemek için kullanılacak.
liste = test_data.index.strftime('%Y-%m-%d')
tahmin_gunu = pd.DataFrame(liste)
tahmin_gunu = tahmin_gunu.shift(+1)
tahmin_gunu.iloc[0:1:] = last_test.index[0].strftime('%Y-%m-%d')
# ---------------------------------------------

# test_data["Tahmin Edilen Gün"] = test_data["Tahmin Edilen Gün"].shift(+1)
# test_data["Tahmin Edilen Gün"].iloc[0:1:] = last_test.index[0].strftime('%Y-%m-%d')

target = target.rename("Hedef")

st.write("-----")

dates = test_data.index



with st.container():

    if secilen_model == 'Lineer Regresyon':
         
        
        element = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)
        st.subheader("Lineer Regresyon")    
        
        test_data = test_data[::-1]
        target = target[::-1]
        
        # ----------------------------------------------
        result = model.predict(test_data.values)
        predictions_lin = pd.DataFrame(result, columns=['Tahmin'])
        predictions_lin["Hedef"] = target.values
        predictions_lin["Date"] = target.index
        predictions_lin.set_index("Date", inplace=True)
        model.fit(test_data.values, target.values)
        
        # ----------------------------------------------
        farklar = []
        for i in predictions_lin.iterrows(): 
            tahmin = i[1]["Tahmin"] 
            gercek = i[1]["Hedef"]
            result = tahmin - gercek
            farklar.append(result) 
            
        predictions_lin["Fark"] = farklar
        # ----------------------------------------------

        st.dataframe(predictions_lin, use_container_width=True)    
        element.add_rows(predictions_lin[["Tahmin","Hedef"]])
        
        # ---------------------------------------------- 
        r2 = calculate_r2_score(predictions_lin["Hedef"], predictions_lin["Tahmin"])
        rmse = np.sqrt(mean_squared_error(predictions_lin["Hedef"], predictions_lin["Tahmin"]))
        mse = mean_squared_error(predictions_lin["Hedef"], predictions_lin["Tahmin"])
        # ----------------------------------------------
        col_r2, col_rmse, col_mse =  st.columns(3)
            
        with col_r2:
            st.subheader("R2 Score")
            st.write(r2)
            
        with col_rmse:
            st.subheader("RMSE")
            st.write(rmse)
            
        with col_mse:
            st.subheader("MSE")
            st.write(mse)
        
        farklar60 = [1,2,3]
        
    if secilen_model == 'Yapay Sinir Ağları':
        
        element = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)
        dates = target.index
        
        st.subheader("Yapay Sinir Ağları")
        test_data_normalize = scaler_X.transform(test_data)
        test_data = pd.DataFrame(test_data_normalize, columns=test_data.columns)
        test_data.index = dates

        target_normalize = scaler_y.transform(target.values.reshape(-1, 1))
        target = pd.DataFrame(target_normalize, columns=['Hedef'])
        target.index = dates
        
        predictions_nn = pd.DataFrame(columns=['Tahmin', 'Hedef'])



        target = target[::-1]
        test_data = test_data[::-1]
        
        for i in range(0, len(test_data), 5):
            
            result = model.predict(test_data.iloc[i:i+5].values)
            result_ = scaler_y.inverse_transform(result)
            real_   = scaler_y.inverse_transform( target.iloc[i:i+5].values)
            temp_df = pd.DataFrame(result_, columns=['Tahmin'])
            temp_df["Hedef"] = real_ 
            temp_df["Date"] = target.iloc[i:i+5].index
            temp_df.set_index("Date", inplace=True)
            predictions_nn = predictions_nn.append(temp_df)
            model.train_on_batch(test_data.iloc[i:i+5].values, target.iloc[i:i+5].values)

        result2 = model.predict(test_data.values) 
        result2 = scaler_y.inverse_transform(result2) 
        predictions_nn60 = pd.DataFrame(result2, columns=['Tahmin'])
        predictions_nn60["Hedef"] = scaler_y.inverse_transform(target.values)
        predictions_nn60["Date"] = target.index 
        predictions_nn60.set_index("Date", inplace=True)
        predictions_nn60["Tahmin Edilen Hedef Günün Kapanışı"] = tahmin_gunu.values

        farklar = []
        for i in predictions_nn.iterrows(): 
            tahmin = i[1]["Tahmin"] 
            gercek = i[1]["Hedef"]
            result = tahmin - gercek
            farklar.append(result) 
            
        predictions_nn["Fark"] = farklar
        
        farklar60 = []
        for i in predictions_nn60.iterrows(): 
            tahmin = i[1]["Tahmin"] 
            gercek = i[1]["Hedef"]
            result = tahmin - gercek 
            farklar60.append(result) 
            
        predictions_nn60["Fark"] = farklar60
        
        
        st.write("----")
        st.subheader("5 günlük güncelleme ile deneme")
        
        r2 = calculate_r2_score(predictions_nn["Hedef"], predictions_nn["Tahmin"])
        rmse = np.sqrt(mean_squared_error(predictions_nn["Hedef"], predictions_nn["Tahmin"]))
        mse = mean_squared_error(predictions_nn["Hedef"], predictions_nn["Tahmin"])
        mae = mean_absolute_error(predictions_nn["Hedef"], predictions_nn["Tahmin"])
        
        element.add_rows(predictions_nn[["Tahmin","Hedef"]])
     
        col_r2, col_rmse, col_mse, col_mae =  st.columns(4)
        
        with col_r2:
            st.subheader("R2 Score")
            st.write(r2)
            
        with col_rmse:
            st.subheader("RMSE")
            st.write(rmse)
            
        with col_mse:
            st.subheader("MSE")
            st.write(mse)
            
        with col_mae:
            st.subheader("Ortalama Mutlak Hata")
            st.write(mae)
        
        st.dataframe(predictions_nn, use_container_width=True)    
        
        
        
        
        
        element_ = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)
        element_.add_rows(predictions_nn60[["Tahmin","Hedef"]])
        
        st.write("----")
        st.subheader("60 günlük deneme")
    
        r2_ = calculate_r2_score(predictions_nn60["Hedef"], predictions_nn60["Tahmin"])
        rmse_ = np.sqrt(mean_squared_error(predictions_nn60["Hedef"], predictions_nn60["Tahmin"]))
        mse_ = mean_squared_error(predictions_nn60["Hedef"], predictions_nn60["Tahmin"])
        mae_ = mean_absolute_error(predictions_nn60["Hedef"], predictions_nn60["Tahmin"])
        
        col_r2_, col_rmse_, col_mse_, col_mae_ =  st.columns(4)
        
        with col_r2_:
            st.subheader("R2 Score")
            st.write(r2_)
            
        with col_rmse_:
            st.subheader("RMSE")
            st.write(rmse_)
            
        with col_mse_:
            st.subheader("MSE")
            st.write(mse_)
            
        with col_mae_:
            st.subheader("Ortalama Mutlak Hata")
            st.write(mae_)
            
        st.dataframe(predictions_nn60, use_container_width=True)
        
        
    if secilen_model == 'LSTM':
        
        
        st.subheader("LSTM")

        element = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)
        dates = target.index
       
       
        test_data_normalize = normalize_data_x(test_data, scaler_X)
        test_data = pd.DataFrame(test_data_normalize, columns=test_data.columns)
        test_data.index = dates
        
        target_normalize = scaler_y.transform(target.values.reshape(-1, 1))
        target = pd.DataFrame(target_normalize, columns=['Hedef'])
        target.index = dates
        predictions_lstm = pd.DataFrame(columns=['Tahmin', 'Hedef'])
        
        target = target[::-1]
        test_data = test_data[::-1]
        
        predictions_l60 = model.predict(test_data.values.reshape(test_data.shape[0], 1, test_data.shape[1]))
        predictions_l60 = scaler_y.inverse_transform(predictions_l60)
        predictions_l60 = pd.DataFrame(predictions_l60, columns=['Tahmin'])
        real   = scaler_y.inverse_transform(target.values.reshape(target.shape[0], 1))
        predictions_l60["Hedef"] = real
        predictions_l60["Date"] = target.index
        predictions_l60.set_index("Date", inplace=True)
        # +1 eklenmiş tarih (bulmak istediğimiz tarih)
        predictions_l60["Tahmin Edilen Hedef Günün Kapanışı"] = tahmin_gunu[::-1].values
        
        for i in range(0, len(test_data), 5):

            result = model.predict(test_data.iloc[i:i+5].values.reshape(test_data.iloc[i:i+5].shape[0], 1, test_data.iloc[i:i+5].shape[1]))
            result = scaler_y.inverse_transform(result) 
            real   = scaler_y.inverse_transform(target.iloc[i:i+5].values.reshape(target.iloc[i:i+5].shape[0], 1))
            temp_df = pd.DataFrame(result, columns=['Tahmin'])
            temp_df["Hedef"] = real
            temp_df["Date"] = target.iloc[i:i+5].index
            temp_df.set_index("Date", inplace=True)
            predictions_lstm = predictions_lstm.append(temp_df)
            model.fit( test_data.iloc[i:i+5].values.reshape(test_data.iloc[i:i+5].shape[0], 1, test_data.iloc[i:i+5].shape[1]), target.iloc[i:i+5].values.reshape(target.iloc[i:i+5].values.shape[0], 1) )
        


        
        
        # predictions_2 içerisindeki her satırı döndürüyoruz.
        farklar = []
        for i in predictions_lstm.iterrows(): 
            tahmin = i[1]["Tahmin"] 
            gercek = i[1]["Hedef"]
            result = tahmin - gercek
            farklar.append(result) 
        predictions_lstm["Fark"] = farklar
        
        
        farklar60 = []
        for i in predictions_l60.iterrows(): 
            tahmin = i[1]["Tahmin"] 
            gercek = i[1]["Hedef"]
            result = tahmin - gercek
            farklar60.append(result) 
        predictions_l60["Fark"] = farklar60
        
        
        st.write("----")
        st.subheader("5 günlük güncelleme ile deneme")
        
        r2 = calculate_r2_score(predictions_lstm["Hedef"], predictions_lstm["Tahmin"])
        rmse = np.sqrt(mean_squared_error(predictions_lstm["Hedef"], predictions_lstm["Tahmin"]))
        mse = mean_squared_error(predictions_lstm["Hedef"], predictions_lstm["Tahmin"])
        mae = mean_absolute_error(predictions_lstm["Hedef"], predictions_lstm["Tahmin"])
        
        element.add_rows(predictions_lstm[["Tahmin","Hedef"]])
        
        col_r2, col_rmse, col_mse, col_mae =  st.columns(4)
        
        with col_r2:
            st.subheader("R2 Score")
            st.write(r2)
            
        with col_rmse:
            st.subheader("RMSE")
            st.write(rmse)
            
        with col_mse:
            st.subheader("MSE")
            st.write(mse)
        with col_mae:
            st.subheader("Ortalama Mutlak Hata")
            st.write(mae)
            
        st.dataframe(predictions_lstm, use_container_width=True)  
        
        st.write("----")
        st.subheader("60 günlük deneme")
        
        r2_ = calculate_r2_score(predictions_l60["Hedef"], predictions_l60["Tahmin"])
        rmse_ = np.sqrt(mean_squared_error(predictions_l60["Hedef"], predictions_l60["Tahmin"]))
        mse_ = mean_squared_error(predictions_l60["Hedef"], predictions_l60["Tahmin"])
        mae_ = mean_absolute_error(predictions_l60["Hedef"], predictions_l60["Tahmin"])
       
        element_lstm_2 = st.line_chart(data=data_frame[["Close"]],  use_container_width=True)
        element_lstm_2.add_rows(predictions_l60[["Tahmin","Hedef"]])
        
        col_r2_, col_rmse_, col_mse_, col_mae_ =  st.columns(4)
        
        with col_r2_:
            st.subheader("R2 Score")
            st.write(r2_)
            
        with col_rmse_:
            st.subheader("RMSE")
            st.write(rmse_)
            
        with col_mse_:
            st.subheader("MSE")
            st.write(mse_)
        with col_mae_:
            st.subheader("Ortalama Mutlak Hata")
            st.write(mae_)
        st.dataframe(predictions_l60, use_container_width=True)
    # Farklar listesinin mutlak değerinin ortalaması 
    
    
    farklar = np.array(farklar)
    farklar = np.abs(farklar)
    farklar = np.mean(farklar)
    
    st.write("5 günlük aralıkla deneme için fark: ", farklar)
    farklar2 = np.array(farklar60)
    farklar2 = np.abs(farklar60)
    farklar2    = np.mean(farklar60)
    
    st.write("60 günlük deneme için fark: ", farklar2)
    
       
    st.write("-----")
    
    st.header("Sonraki günün tahmini")
    st.write(f"Son gün ({last_test.index[0].strftime('%Y-%m-%d')}) kullanılarak sonraki kapanış tahmini yapılırsa :   ")
    
    last_day = last_test.index[0]
    gercek = last_test["Close"].values[0]
    
    if secilen_model == 'Lineer Regresyon':
        result = model.predict(last_test.values)
        
    if secilen_model == 'Yapay Sinir Ağları':
        st.write(last_test)
        last_test_norm = scaler_X.transform(last_test)
        result = model.predict(last_test_norm)
        result = scaler_y.inverse_transform(result)
        
    
    if secilen_model == 'LSTM':
        st.write(last_test)
        last_test_norm = normalize_data_x(last_test, scaler_X)
        result = model.predict(last_test_norm.reshape(last_test.shape[0], 1, last_test.shape[1]))
        result = scaler_y.inverse_transform(result)
        
    color = "green"
        
    with open("./css/style.css") as source:
        style = source.read()    
   
    last_day = last_test.iloc[0:1:].index[0]
    
    with st.container():
        st.write(str(last_day).split()[0])
        
        component.html(f"""
        <style>
            {style}
        </style>
        <div class="kapanis-fiyati">
            <p style="margin:15px;">
                {str(last_day).split()[0]} Kapanış fiyatı : <span class="gercek-fiyat"> {gercek}₺ </span>
            </p>
        </div>
            </br>
        <div class="model-tahmin-fiyati" style="background-color: {color}">
            <h3 style="margin:15px;">
                Modelin sonraki kapanış için tahmini :   <span class="tahmin-fiyat"> {tahmin}₺ </span>
            </h3>               
        </div>         
            """, height=300 )    
        
    

        
        
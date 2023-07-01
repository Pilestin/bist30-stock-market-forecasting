import pandas as pd


import ta.momentum as momentum
import ta.volatility as volatility 
import ta.volume as volume
import ta.trend as trend
import ta.others as others



class BistIndicators:
    
    def __init__(self,data_frame) -> None:
        self.indicators = { 
                    "SMA": trend.SMAIndicator(close=data_frame["Close"], window=20, fillna=True).sma_indicator(),  
                    "EMA": trend.EMAIndicator(close=data_frame["Close"], window=20, fillna=True).ema_indicator(), 
                    "WMA": trend.WMAIndicator(close=data_frame["Close"], window=20, fillna=True).wma(),
                    "MACD": trend.MACD(close=data_frame["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=True).macd(),  
                    "Aroon": trend.AroonIndicator(close=data_frame["Close"], window=25, fillna=True).aroon_indicator(), 
                    "DPO": trend.DPOIndicator(close=data_frame["Close"], window=20, fillna=True).dpo(),  
                    "KST": trend.KSTIndicator(close=data_frame["Close"], window1=30, window2=10, window3=10, window4=9, fillna=True).kst(), 
                    "MASS": trend.MassIndex(high=data_frame["High"], low=data_frame["Low"], window_fast=9, window_slow=25, fillna=True).mass_index(),  
                    "PSAR": trend.PSARIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], step=0.02, max_step=0.2, fillna=True).psar(),  
                    "TRIX": trend.TRIXIndicator(close=data_frame["Close"], window=15, fillna=True).trix(),  
                    "VORTEX": trend.VortexIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window=14, fillna=True).vortex_indicator_diff(),  
                    "CCI": trend.CCIIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window=20, constant=0.015, fillna=True).cci(),  

                    # Volatilite İndikatörleri
                    "BBB": volatility.BollingerBands(close=data_frame["Close"], window=20, window_dev=2, fillna=True).bollinger_mavg(),  
                    # "ATR": volatility.AverageTrueRange(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window=14, fillna=True).average_true_range(),  
                    "KC": volatility.KeltnerChannel(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window=20, window_atr=10, fillna=True).keltner_channel_mband(),

                    # Momentum İndikatörleri
                    "RSI": momentum.RSIIndicator(close=data_frame["Close"], window=14, fillna=True).rsi(), 
                    "STOCHRSI": momentum.StochRSIIndicator(close=data_frame["Close"], window=14, smooth1=3, smooth2=3, fillna=True).stochrsi(),
                    "AO": momentum.AwesomeOscillatorIndicator(high=data_frame["High"], low=data_frame["Low"], window1=5, window2=34, fillna=True).awesome_oscillator(), 
                    "KAMA": momentum.KAMAIndicator(close=data_frame["Close"], window=10, pow1=2, pow2=30, fillna=True).kama(),  
                    "TSI": momentum.TSIIndicator(close=data_frame["Close"], window_slow=25, window_fast=13, fillna=True).tsi(),  
                    "UO": momentum.UltimateOscillator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window1=7, window2=14, window3=28, weight1=4.0, weight2=2.0, weight3=1.0, fillna=True).ultimate_oscillator(),  
                    "Stoch": momentum.StochasticOscillator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window=14, smooth_window=3, fillna=True).stoch(),  
                    "WILL": momentum.WilliamsRIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], lbp=14, fillna=True).williams_r(), 
                    "PERC": momentum.PercentagePriceOscillator(close=data_frame["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=True).ppo_signal(),  

                    # Hacim İndikatörleri
                    "OBV": volume.OnBalanceVolumeIndicator(close=data_frame["Close"], volume=data_frame["Volume"], fillna=True).on_balance_volume(),  
                    "VWAP": volume.VolumeWeightedAveragePrice(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], window=14, fillna=True).volume_weighted_average_price(), 
                    "VPT": volume.VolumePriceTrendIndicator(close=data_frame["Close"], volume=data_frame["Volume"], fillna=True).volume_price_trend(),  
                    "FI": volume.ForceIndexIndicator(close=data_frame["Close"], volume=data_frame["Volume"], window=13, fillna=True).force_index(),  
                    "CMF": volume.ChaikinMoneyFlowIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], window=20, fillna=True).chaikin_money_flow(), 
                    "EOM": volume.EaseOfMovementIndicator(high=data_frame["High"], low=data_frame["Low"], volume=data_frame["Volume"], window=14, fillna=True).ease_of_movement(),  
                    "MFI": volume.MFIIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], window=14, fillna=True).money_flow_index(),
                    "ADI": volume.AccDistIndexIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], fillna=True).acc_dist_index(),
                    }
        
    def set_indicators(self,data_frame, options)-> pd.DataFrame:
        
        for ind in options: 
            data_frame[ind] = self.indicators[ind]
            
        return data_frame
   
   
   
     
def get_indicators(data_frame):
    """ VERİ ÇERÇEVESİNİ ALIR VE İNDİKATÖRLERİNİ OLUŞTURUR. """
    

    indicators={"RSI" : momentum.RSIIndicator(close=data_frame["Close"], window = 14, fillna=True).rsi(), 
                "AO"  : momentum.AwesomeOscillatorIndicator(high=data_frame["High"], low=data_frame["Low"], window1=5, window2=34, fillna=True).awesome_oscillator(),
                "KAMA": momentum.KAMAIndicator(close=data_frame["Close"], window=10, pow1=2, pow2=30, fillna=True).kama(),
                "TSI" : momentum.TSIIndicator(close=data_frame["Close"], window_slow=25, window_fast=13, fillna=True).tsi(),
                "UO"  : momentum.UltimateOscillator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], window1=7, window2=14, window3=28, weight1=4.0, weight2=2.0, weight3=1.0, fillna=True).ultimate_oscillator(),
                "BBB" : volatility.BollingerBands(close=data_frame["Close"], window=20, window_dev=2, fillna=True).bollinger_mavg(),
                "SMA" : trend.SMAIndicator(close=data_frame["Close"], window=20,fillna=True).sma_indicator(),
                "EMA" : trend.EMAIndicator(close=data_frame["Close"], window=20,fillna=True).ema_indicator(),
                "MACD": trend.MACD(close=data_frame["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=True).macd_signal(),
                "OBV" : volume.OnBalanceVolumeIndicator(close=data_frame["Close"], volume=data_frame["Volume"],fillna=True).on_balance_volume(),
                "VWAP": volume.VolumeWeightedAveragePrice(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], window=14, fillna=True).volume_weighted_average_price(),
                "VPT" : volume.VolumePriceTrendIndicator(close=data_frame["Close"], volume=data_frame["Volume"], fillna=True).volume_price_trend(),
                "FI"  : volume.ForceIndexIndicator(close=data_frame["Close"], volume=data_frame["Volume"], window=13, fillna=True).force_index(),
                "CMF" : volume.ChaikinMoneyFlowIndicator(high=data_frame["High"], low=data_frame["Low"], close=data_frame["Close"], volume=data_frame["Volume"], window=20, fillna=True).chaikin_money_flow(),
                "EOM" : volume.EaseOfMovementIndicator(high=data_frame["High"], low=data_frame["Low"], volume=data_frame["Volume"], window=14, fillna=True).ease_of_movement(),
                }
    
    return indicators

choosen = ['Open', 'High', 'Low', 'Volume'] 

def set_indicators(data_frame, options):
    """ VERİ ÇERÇEVESİNİ, İNDİKATÖR LİSTESİNİ ALIR, BUNLARI VERİ ÇERÇEVESİNE EKLER."""
     
    indicators = get_indicators(data_frame)
     
    for i in options: 
        data_frame[i] = indicators[i]
        
    for i in options:
        choosen.append(i)
    
    return data_frame, choosen  # choosen : seçilen indikatörlerin listesi. 

import yfinance as yf
from datetime import datetime as date

# Bu sınıf veriler için dataframe oluşturacaktır. 
# Web tarafından girilen tüm tercihleri toplar ve bir dataframe oluşturur.


class CurrentData():
    
    def __init__(self,begin_time, end_time, bist_dict ,choosen):
        
        self.begin_time  = begin_time
        self.end_time    = end_time 
        self.bist_dict  = bist_dict 
        self.choosen = choosen       # KOCHOLDING gibi bir şey gelecek.(HİSSE İSMİ)
        self.download() 
        self.control_volume()
        
    def download(self):
        self.df = yf.download(self.bist_dict[self.choosen], 
                start=str(self.begin_time),
                end=str(self.end_time))
        
        return self.df
    
    def direct_download(self, begin, end):
        df = yf.download("XU030.IS", begin, end )
 
        return self.df
    
    def control_volume(self):
        # Eğer son günün hacmi 0 ise, son 10 günün ortalamasını alıyoruz. 
        if self.df.loc[self.df.index[-1], 'Volume'] == 0:
            
            son_10 = self.df.tail(10) 
            ortalama_son_10 = son_10["Volume"].mean()
            self.df.loc[self.df.index[-1], 'Volume'] = ortalama_son_10
    




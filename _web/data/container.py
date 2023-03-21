import requests
from bs4 import BeautifulSoup as BS

_bist30 = {"BIST30":"XU030.IS", "BIST100":"XU100.IS",}

def getBistInfo():
    """
        Bu fonksiyon url içerisindeki bist30 şirketlerinin isim ve kod bilgilerini döndürür.
    """
    web_site = requests.get('https://borsa.doviz.com/hisseler').content
    soup = BS(web_site,'html.parser')
    
    # sayfa içerisinde id=stocks olan table bulunmakta
    table = soup.find("table",{"id": "stocks"})

    # tablo içerisinde class=currency-details olan div'i alıcaz. 
    rows   = table.find_all("div",{"class": "currency-details"}) # Sonuçlar liste şeklinde gelecek.

    # çektiğimiz bilginin ilk elemanı şu şekilde : 
    # 
    # <div class="currency-details">
    #   <div>ISCTR</div>
    #   <div class="cname">IS BANKASI (C)</div>
    # </div>
    # 
    
    def first30():
        
        sayac = 1
        for row in rows:
        
            # burada her bir satır gelecek. Bu satırı sırasıyla text'ini alıcaz. Ardından da boşlukları atacağız.
            hisse_bilgisi = row.text.split()
            
            # ['ISCTR', 'IS', 'BANKASI', '(C)']
            # . . . 
            # Ve bu bilgilerin ilkini alacağız 
            
            hisse_kodu = hisse_bilgisi[0] + ".IS"              # listenin ilk elemanı hisse kodu
            hisse_adi  = "".join(hisse_bilgisi[1:])    # listenin geri kalanı hisse ismi, string yapılmalı
            _bist30[hisse_adi] = hisse_kodu             # ve dictionary yapısına eklenir
            
            if sayac==30:
                break
            sayac += 1 
            
    first30()
    return _bist30


from datetime import datetime as date

today = date.today().strftime('%Y-%m-%d')       # ["2023","3","20"] 
_today = [int(i) for i in today.split("-")] 


print(_today)
print(today)

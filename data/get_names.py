# hisse ve endeklerin getirilmesini sağlar.
# Bu bilgileri bir listede tutar ve döndürür. 
# request  ve bs4 ile borsa kaynağından çekildi. (doviz.com)


import requests
from bs4 import BeautifulSoup as BS

# "Hisse Adı" : "Hisse Kodu
_kisaltmalar = {"BIST30":"XU030.IS", "BIST100":"XU100.IS"}

def getBistInfo() -> dict:
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
            
            hisse_kodu = hisse_bilgisi[0] + ".IS"            # listenin ilk elemanı hisse kodu
            hisse_adi  = "".join(hisse_bilgisi[1:])          # listenin geri kalanı hisse ismi, string yapılmalı
            _kisaltmalar[hisse_adi] = hisse_kodu             # ve dictionary yapısına eklenir
            
            sayac += 1 
            
            if sayac==30:
                break
            
    first30()
    
    return _kisaltmalar



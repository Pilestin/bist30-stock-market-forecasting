import yfinance as yf

def bist30(start, end):
        
    df =  yf.download("XU030.IS",
                start= start, # start= "2020-09-22",
                end= end)   # end= "2023-05-20")
    
    return df
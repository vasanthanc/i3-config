from i3pystatus import IntervalModule
from i3pystatus.core.util import internet, require
from nsetools import Nse
import time
import urllib.request

class Nifty50 (IntervalModule):
    on_upscroll = ["scroll_format", 1]
    on_downscroll = ["scroll_format", -1]
    format = "{symbol} {status}{change_price}({pchange}%) {last_price} {currency} {time}"
    currency = "INR"
    interval = 5
    symbols = ['NIFTY 50', 'NIFTY BANK', 'APOLLOTYRE','BAJAJ-AUTO','BHARTIARTL','BRITANNIA','CANBK','CROMPTON','EBBETF0430','EICHERMOT','ESCORTS','FORCEMOT','GOLDBEES','HAVELLS','HDFCBANK','HINDALCO','HINDUNILVR','HINDZINC','ICICILOVOL','ICICINIFTY','ICICINV20','ICICINXT50','INFY','IRFC','JINDALSTEL','JUNIORBEES','L&TFH','LIQUIDBEES','LT','LTTS','M&M','MIDHANI','MOIL','MON100','NATIONALUM','NETFMID150','NIFTYBEES','NMDC','ORIENTCEM','ORIENTELEC','POWERGRID','SBIN','SGIL','SOUTHBANK','TATAMETALI','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','UJAAS','UNIONBANK','VBL','WIPRO']
    #symbols = ['EBBETF0430','EICHERMOT','ESCORTS','FORCEMOT','HAVELLS','HDFCBANK','HINDALCO','HINDUNILVR','HINDZINC','ICICILOVOL','ICICINIFTY','ICICINV20','ICICINXT50','INFY','IRFC','JINDALSTEL','JUNIORBEES','L&TFH','LIQUIDBEES','LT','LTTS','M&M','MIDHANI','MOIL','MON100','NATIONALUM','NETFMID150','NIFTYBEES','NMDC','ORIENTCEM','ORIENTELEC','POWERGRID','SBIN','SGIL','SOUTHBANK','TATAMETALI','TATAMOTORS','TATAPOWER','TATASTEEL','TECHM','UJAAS','UNIONBANK','VBL','WIPRO']
    color_up = "#00FF00"
    color_down = "#FF0000"
    color = "#FFFFFF"
    colorize = False
    status = {
        "price_up": "▲",
        "price_down": "▼",
    }

    def check_negative(self, s):
        try:
            f = float(s)
            if (f < 0):
                return True
            # Otherwise return false
            return False
        except ValueError:
            return False

    def init(self):
        self.current_symbol_index = 0
        self.last_scroll_count = 1
        self.get_symbol_name = "https://www.moneycontrol.com/mccode/common/autosuggestion_solr.php?classic=true&query={}&type=1&format=json"
        self.get_equity_cash = "https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/{}"

    @require(internet)
    def run(self):
        #print (self.current_symbol_index)
        #self.current_symbol_index = 0
        #print ({"a":self.current_symbol_index})
        self.symbol = Nifty50.symbols[self.current_symbol_index]
        nse = Nse()
        #for i in range (0,200):
        while True:
            try:
                #print ("HI")
                #print (self.symbol)
                if "NIFTY" in self.symbol:
                    index_info = nse.get_index_quote(self.symbol)
                else:
                    index_info = nse.get_quote(self.symbol)
                if not index_info:
                    raise Exception ("NO DATA FOUND")
                #print (index_info)
                #break
            except Exception as e:
                #print (str(e))
                if self.current_symbol_index >= len(Nifty50.symbols):
                    self.current_symbol_index = 0
                    self.last_scroll_count = -1
                if self.current_symbol_index < 0:
                    self.current_symbol_index = len(Nifty50.symbols)-1
                    self.last_scroll_count = 1
                self.current_symbol_index+= self.last_scroll_count
                self.symbol = Nifty50.symbols[self.current_symbol_index]
                continue
            else:
                break
        #print (index_info)
        current_price = index_info.get('lastPrice', None)
        change_price = index_info.get('change', None)
        pchange = index_info.get('pChange', None)
        if self.check_negative(change_price):
            status = self.status["price_down"]
            color = self.color_down
        else:
            color = self.color_up
            status = self.status["price_up"]
        fdict = {
            "symbol": self.symbol,
            "last_price": current_price,
            "currency": self.currency,
            "change_price": change_price,
            "pchange": pchange,
            "status": status,
            "time": int(time.time())
        }
        self.data = fdict
        self.output = {
            "full_text": self.format.format(**fdict),
            "color": color,
        }
        # print(self.output)

    def scroll_format(self, intervalo=1):
        #print ("clicke")
        self.last_scroll_count = intervalo
        self.current_symbol_index += intervalo
        if self.current_symbol_index >= len(Nifty50.symbols):
            self.current_symbol_index = 0
        if self.current_symbol_index < 0:
            self.current_symbol_index = len(Nifty50.symbols)-1

        #self.output["full_text"] = "------{}".format(interval)

if __name__ == '__main__':
    nft = Nifty50()
    nft.run()

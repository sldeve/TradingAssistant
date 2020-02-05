class Position:

    def __init__(self, symbol, position_size, position_value, entry, market_price, liquidation_price, margin, leverage, unrealised_pnl, realised_pnl):
        self.symbol = symbol
        self.position_size = position_size
        self.position_value = position_value
        self.entry = entry
        self.market_price = market_price
        self.liquidation_price = liquidation_price
        self.margin = margin
        self.leverage = leverage
        self.unrealised_pnl = unrealised_pnl
        self.realised_pnl = realised_pnl
        if (liquidation_price > entry):
            self.direction = "Short"
        else:
            self.direction = "Long"

    def get_symbol(self):
        return self.symbol

    def get_position_size(self):
        return self.position_size

    def get_position_value(self):
        return self.position_value

    def get_entry(self):
        return self.entry

    def get_market_price(self):
        return self.market_price

    def get_liquidation_price(self):
        return self.liquidation_price

    def get_margin(self):
        return self.margin

    def get_leverage(self):
        return self.leverage

    def get_unrealised_pnl(self):
        return self.unrealised_pnl

    def get_realised_pnl(self):
        return self.realised_pnl

    def set_symbol(self, t):
        self.symbol = t

    def set_position_size(self, ps):
        self.position_size = ps

    def set_position_value(self, pv):
        self.position_value = pv

    def set_entry(self, e):
        self.entry = e

    def set_market_price(self, mp):
        self.market_price = mp

    def set_liquidation_price(self, lp):
        self.liquidation_price = lp

    def set_margin(self, m):
        self.margin = m

    def set_leverage(self, l):
        self.leverage = l

    def set_unrealised_pnl(self, p):
        self.unrealised_pnl = p

    def set_realised_pnl(self, p):
        self.realised_pnl = p

    def __str__(self):
        return "Instrument: " + self.symbol + "\n" +"Direction: "+ self.direction +"\n" + "Position Size: " + str(self.position_size) + " Contracts" +"\n" + "Value: " + str(abs(self.position_value / 100000000)) + " XBT" + "\n" + "Entry Price: $" + str(self.entry) + "\n" + "Market Price: $" + str(self.market_price) + "\n" +"Liquidation Price: $" + str(self.liquidation_price) + "\n" + "Margin: " + str(self.margin / 100000000) + " XBT" +"\n" + "Leverage: " + str(self.leverage) +"x" + "\n" + "Unrealised PNL: " + str(format(self.unrealised_pnl / 100000000, 'f')) + " XBT" + "\n" + "Realised PNL: " + str(format(self.realised_pnl / 100000000, 'f')) + " XBT" + "\n"

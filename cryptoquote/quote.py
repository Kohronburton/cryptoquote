"""Classes for handling price quotes on an exchange for a pair of assets"""

from datetime import datetime

class Quote(object):
    """Represents a price quote for a pair of assets on an exchange"""

    def __init__(self, exchange, base_asset, quote_asset, ask_price=None,
                 bid_price=None, last_trade_price=None, today_low=None,
                 today_high=None, today_avg=None, twenty_four_low=None,
                 twenty_four_high=None, twenty_four_avg=None, time=None):
        """Instantiates a new quote

        :param exchange: exchange name
        :type exchange: str
        :param base_asset: base asset the quote represents
        :type base_asset: :class:`~cryptoprice.asset.BaseAsset`
        :param quote_asset: quote asset the quote represents
        :type quote_asset: :class:`~cryptoprice.asset.BaseAsset`
        :param ask_price: ask price
        :type ask_price: float
        :param bid_price: bid price
        :type bid_price: float
        :param last_trade_price: last trade price
        :type last_trade_price: float
        :param today_low: today's lowest price
        :type today_low: float
        :param today_high: today's highest price
        :type today_high: float
        :param today_avg: today's average price
        :type today_avg: float
        :param twenty_four_low: lowest price in last 24h
        :type twenty_four_low: float
        :param twenty_four_high: highest price in last 24h
        :type twenty_four_high: float
        :param twenty_four_avg: average price in last 24h
        :type twenty_four_avg: float
        :param time: quote time
        :type time: :class:`datetime.datetime`
        """

        # validate inputs
        self.exchange = str(exchange)
        self.base_asset = base_asset
        self.quote_asset = quote_asset

        if ask_price is not None:
            ask_price = float(ask_price)

        if bid_price is not None:
            bid_price = float(bid_price)

        if last_trade_price is not None:
            last_trade_price = float(last_trade_price)

        if today_low is not None:
            today_low = float(today_low)

        if today_high is not None:
            today_high = float(today_high)

        if today_avg is not None:
            today_avg = float(today_avg)

        if twenty_four_low is not None:
            twenty_four_low = float(twenty_four_low)

        if twenty_four_high is not None:
            twenty_four_high = float(twenty_four_high)

        if twenty_four_avg is not None:
            twenty_four_avg = float(twenty_four_avg)

        if time is None:
            time = datetime.now()

        self.ask_price = ask_price
        self.bid_price = bid_price
        self.last_trade_price = last_trade_price
        self.today_low = today_low
        self.today_high = today_high
        self.today_avg = today_avg
        self.twenty_four_low = twenty_four_low
        self.twenty_four_high = twenty_four_high
        self.twenty_four_avg = twenty_four_avg
        self.time = time

    def __str__(self):
        """String representation of quote

        :return: quote information
        :rtype: str
        """

        return self.info()

    def info(self):
        """Get quote information

        :return: quote information
        :rtype: str
        """

        # locale-aware time
        time_str = self.time.strftime("%x %X")

        # prices
        if self.ask_price is not None:
            ask_price_str = self.quote_asset.formatted_value(self.ask_price)
        else:
            ask_price_str = "?"

        if self.bid_price is not None:
            bid_price_str = self.quote_asset.formatted_value(self.bid_price)
        else:
            bid_price_str = "?"

        if self.last_trade_price is not None:
            last_trade_price_str = self.quote_asset.formatted_value(self.last_trade_price)
        else:
            last_trade_price_str = "?"

        if self.today_low is not None:
            today_low_str = self.quote_asset.formatted_value(self.today_low)
        else:
            today_low_str = "?"

        if self.twenty_four_low is not None:
            twenty_four_low_str = self.quote_asset.formatted_value(self.twenty_four_low)
        else:
            twenty_four_low_str = "?"

        if self.today_high is not None:
            today_high_str = self.quote_asset.formatted_value(self.today_high)
        else:
            today_high_str = "?"

        if self.twenty_four_high is not None:
            twenty_four_high_str = self.quote_asset.formatted_value(self.twenty_four_high)
        else:
            twenty_four_high_str = "?"

        if self.today_avg is not None:
            today_avg_str = self.quote_asset.formatted_value(self.today_avg)
        else:
            today_avg_str = "?"

        if self.twenty_four_avg is not None:
            twenty_four_avg_str = self.quote_asset.formatted_value(self.twenty_four_avg)
        else:
            twenty_four_avg_str = "?"

        return ("%s price on %s as of %s:\n"
               "\tAsk: %s\n"
               "\tBid: %s\n"
               "\tLast: %s\n"
               "\tToday low: %s (last 24h: %s)\n"
               "\tToday high: %s (last 24h: %s)\n"
               "\tToday average: %s (last 24h: %s)") % (
               self.base_asset,
               self.exchange,
               time_str,
               ask_price_str,
               bid_price_str,
               last_trade_price_str,
               today_low_str,
               twenty_four_low_str,
               today_high_str,
               twenty_four_high_str,
               today_avg_str,
               twenty_four_avg_str
        )

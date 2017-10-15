"""Classes for handling price quotes on an exchange for a pair of assets"""

from datetime import datetime

class Quote(object):
    """Represents a price quote for a pair of assets on an exchange"""

    def __init__(self, asset_pair, ask_price=None, bid_price=None,
                 last_trade_price=None, today_low=None, today_high=None,
                 twenty_four_low=None, twenty_four_high=None, time=None):
        """Instantiates a new quote

        :param asset_pair: asset pair the quote represents
        :type asset_pair: :class:`~cryptoprice.asset.BaseAssetPair`
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
        :param twenty_four_low: lowest price in last 24h
        :type twenty_four_low: float
        :param twenty_four_high: highest price in last 24h
        :type twenty_four_high: float
        :param time: (optional) quote time
        :type time: :class:`datetime.datetime`
        """

        # validate inputs
        self.asset_pair = asset_pair
        self.ask_price = float(ask_price)
        self.bid_price = float(bid_price)
        self.last_trade_price = float(last_trade_price)
        self.today_low = float(today_low)
        self.today_high = float(today_high)
        self.twenty_four_low = float(twenty_four_low)
        self.twenty_four_high = float(twenty_four_high)

        if time is None:
            time = datetime.now()

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

        return ("%s price as of %s:\n"
               "\tAsk: %s\n"
               "\tBid: %s\n"
               "\tLast: %s\n"
               "\tToday low: %s (last 24h: %s)\n"
               "\tToday high: %s (last 24h: %s)") % (
            self.asset_pair.base_asset,
            time_str,
            self.asset_pair.quote_asset.formatted_value(self.ask_price),
            self.asset_pair.quote_asset.formatted_value(self.bid_price),
            self.asset_pair.quote_asset.formatted_value(self.last_trade_price),
            self.asset_pair.quote_asset.formatted_value(self.today_low),
            self.asset_pair.quote_asset.formatted_value(self.twenty_four_low),
            self.asset_pair.quote_asset.formatted_value(self.today_high),
            self.asset_pair.quote_asset.formatted_value(self.twenty_four_high),
        )

"""Classes for handling price quotes on an exchange for a pair of assets"""

class Quote(object):
    """Represents a price quote for a pair of assets on an exchange"""

    def __init__(self, asset_pair, ask_price=None, bid_price=None,
                 last_trade_price=None, today_low=None, today_high=None,
                 twenty_four_low=None, twenty_four_high=None):
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

    def __str__(self):
        """String representation of quote

        :return: quote price
        :rtype: str
        """

        # use the last trade price
        price = self.last_trade_price

        return "1 %s\t%s" % (self.asset_pair.crypto_asset,
                             self.asset_pair.fiat_asset.formatted_value(price))

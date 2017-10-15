"""Classes for interacting with cryptocurrency exchanges"""

import abc
import requests

from cryptoprice.asset import KrakenAssetPair
from cryptoprice.quote import Quote

class BaseExchange(object, metaclass=abc.ABCMeta):
    """Object representing a cryptocurrency exchange"""

    @abc.abstractmethod
    def asset_pairs(self):
        """Generates sequence of asset pairs available at this exchange

        :return: asset pairs
        :rtype: sequence of :class:`~cryptoprice.asset.BaseAssetPair`
        """

        return NotImplemented

class Kraken(BaseExchange):
    # asset pairs URL
    ASSET_PAIR_URL = "https://api.kraken.com/0/public/AssetPairs"

    # price URL
    TICKER_URL = "https://api.kraken.com/0/public/Ticker"

    def asset_pairs(self):
        """Generates sequence of asset pairs available at this exchange

        :return: asset pairs
        :rtype: sequence of :class:`~cryptoprice.asset.KrakenAssetPair`
        """

        # get and decode JSON document with asset pairs
        asset_dict = requests.get(self.ASSET_PAIR_URL).json()

        # well-formatted document will contain a "result" field
        if not "result" in asset_dict.keys():
            raise KeyError("Unexpected JSON data received")

        for asset in asset_dict["result"].keys():
            if asset[-2:] == ".d":
                # skip decimal versions
                continue

            yield KrakenAssetPair(asset, asset_dict["result"][asset])

    def quote(self, asset_pair):
        """Returns quote for the specified asset pair

        :param asset_pair: asset pair to quote
        :type asset_pair: :class:`~cryptoprice.asset.BaseAssetPair`
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        # get and decode JSON document with prices
        quote_dict = requests.get(self.ticker_url(asset_pair)).json()

        # well-formatted document will contain a "result" field
        if not "result" in quote_dict.keys():
            raise KeyError("Unexpected JSON data received")

        # extract prices from result dict
        prices = quote_dict["result"][asset_pair.pair_name]

        # build and return quote
        return Quote(asset_pair, ask_price=prices["a"][0],
                     bid_price=prices["b"][0], last_trade_price=prices["c"][0],
                     today_low=prices["l"][0], today_high=prices["h"][0],
                     twenty_four_low=prices["l"][1],
                     twenty_four_high=prices["h"][1])

    def ticker_url(self, asset_pair):
        """Returns URL for the specified asset pair

        :param asset_pair: asset pair to get prices for
        :type asset_pair: :class:`~cryptoprice.asset.BaseAssetPair`
        :return: URL
        :rtype: str
        """

        return self.TICKER_URL + "?pair=%s" % asset_pair.quote_str

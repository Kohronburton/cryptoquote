"""Classes for interacting with cryptocurrency exchanges"""

import abc
import requests
import logging

from .asset import AssetFactory, KrakenAssetPair, BTCAsset
from .quote import Quote
from .cache import read_cache, write_cache, NoCacheException, \
                   InvalidCacheException

class BaseExchange(object, metaclass=abc.ABCMeta):
    """Object representing a cryptocurrency exchange"""

    NAME = ""
    URL = ""

    def quote(self, base_name, quote_name):
        """Returns quote for the specified asset pair

        :param base_name: base asset name, or asset pair name
        :type base_name: str
        :param quote_name: (optional) quote asset name
        :type quote_name: str
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        # parse asset names
        base = AssetFactory.from_str(base_name)
        quote = AssetFactory.from_str(quote_name)

        # check if assets can be handled by this exchange
        if not base.can_handle_exchange(self):
            raise ValueError("%s cannot handle %s asset" % (self.NAME, base))
        if not quote.can_handle_exchange(self):
            raise ValueError("%s cannot handle %s asset" % (self.NAME, quote))

        # handle quote for this exchange
        return self.handle_quote(base, quote)

    @abc.abstractmethod
    def handle_quote(self, base, quote):
        """Returns quote for the specified asset pair

        :param base: base asset
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        return NotImplemented

    def asset_pairs(self):
        """Generates sequence of asset pairs available at this exchange

        By default, returns an empty list. This may be overridden by subclasses
        to return a list of exchange-specific asset pairs.

        :return: asset pairs
        :rtype: sequence of :class:`~cryptoprice.asset.KrakenAssetPair`
        """

        return []

    def assets_to_pair(self, base, quote):
        """Returns the pair name corresponding to the specified assets

        :param base: base asset
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: asset pair
        :rtype: :class:`~cryptoprice.asset.BaseAssetPair`
        :raises ValueError: if assets can't be formed into a known pair
        """

        for pair in self.asset_pairs():
            if base.NAME in pair.base_asset.aliases and quote.NAME in pair.quote_asset.aliases:
                return pair

        raise ValueError("Specified assets cannot be formed into a known pair "
                         "on %s" % self.NAME)

    def __str__(self):
        """String representation"""

        return self.NAME

class Kraken(BaseExchange):
    # basic information
    NAME = "Kraken"
    URL = "https://www.kraken.com/"

    # asset pairs URL
    ASSET_PAIR_URL = "https://api.kraken.com/0/public/AssetPairs"

    # price URL
    TICKER_URL = "https://api.kraken.com/0/public/Ticker"

    def asset_pairs(self):
        """Generates sequence of asset pairs available at this exchange

        :return: asset pairs
        :rtype: sequence of :class:`~cryptoprice.asset.KrakenAssetPair`
        """

        # get asset pairs from cache
        try:
            asset_pair_dict = read_cache("kraken_asset_pairs")
        except (NoCacheException, InvalidCacheException) as e:
            # empty or invalid cache
            logging.getLogger("exchange").info("Asset cache not found")

            # get and decode JSON document with asset pairs
            asset_pair_dict = requests.get(self.ASSET_PAIR_URL).json()

            # save cache
            write_cache(asset_pair_dict, "kraken_asset_pairs")

        # well-formatted document will contain a "result" field
        if not "result" in asset_pair_dict.keys():
            raise KeyError("Unexpected JSON data received")

        for asset_pair in asset_pair_dict["result"].keys():
            if asset_pair[-2:] == ".d":
                # skip decimal versions
                continue

            yield KrakenAssetPair(asset_pair, asset_pair_dict["result"][asset_pair])

    def handle_quote(self, base, quote):
        """Returns quote for the specified asset pair

        :param base: base asset
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        # form Kraken asset pair
        asset_pair = self.assets_to_pair(base, quote)

        # get and decode JSON document with prices
        quote_dict = requests.get(self.ticker_url(asset_pair)).json()

        # well-formatted document will contain a "result" field
        if not "result" in quote_dict.keys():
            raise KeyError("Unexpected JSON data received")

        # extract prices from result dict
        prices = quote_dict["result"][asset_pair.pair_name]

        # build and return quote
        return Quote(self.NAME, asset_pair.base_asset, asset_pair.quote_asset,
                     ask_price=prices["a"][0], bid_price=prices["b"][0],
                     last_trade_price=prices["c"][0], today_low=prices["l"][0],
                     today_high=prices["h"][0], twenty_four_low=prices["l"][1],
                     twenty_four_high=prices["h"][1])

    def ticker_url(self, asset_pair):
        """Returns URL for the specified asset pair

        :param asset_pair: asset pair to get prices for
        :type asset_pair: :class:`~cryptoprice.asset.BaseAssetPair`
        :return: URL
        :rtype: str
        """

        return self.TICKER_URL + "?pair=%s" % asset_pair.quote_str

class LocalBitcoins(BaseExchange):
    # basic information
    NAME = "LocalBitcoins"
    URL = "https://localbitcoins.com/"

    # price URL
    TICKER_URL = "https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/"

    def handle_quote(self, base, quote):
        """Returns quote for the specified asset pair

        :param base: base asset
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        # get and decode JSON document with prices
        quote_dict = requests.get(self.TICKER_URL).json()

        # find quote price in dict
        for currency in quote_dict.keys():
            if currency in quote.aliases:
                # found currency
                prices = quote_dict[currency]

                # build and return quote
                return Quote(self.NAME, base, quote,
                             last_trade_price=prices["rates"]["last"],
                             twenty_four_avg=prices["avg_24h"])

        raise ValueError("%s not quoted on %s" % (quote_name, self.NAME))

class Coinbase(BaseExchange):
    # basic information
    NAME = "Coinbase"
    URL = "https://www.coinbase.com/"

    # price URL
    SPOT_PRICE_URL = "https://api.coinbase.com/v2/prices/{}-{}/spot"

    def handle_quote(self, base, quote):
        """Returns quote for the specified asset pair

        :param base: base asset
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: quote
        :rtype: :class:`~cryptoprice.quote.Quote`
        """

        # get and decode JSON document with prices
        quote_dict = requests.get(self.ticker_url(base, quote)).json()

        # well-formatted document will contain a "data" field
        if not "data" in quote_dict.keys():
            raise KeyError("Unexpected JSON data received")

        # extract prices from result dict
        price = quote_dict["data"]

        if "amount" in price.keys():
            # build and return quote
            return Quote(self.NAME, base, quote,
                         last_trade_price=price["amount"])

        raise ValueError("%s not quoted on %s" % (quote_name, self.NAME))

    def ticker_url(self, base, quote):
        """Returns URL for the specified asset pair

        :param base: base asset to get prices for
        :type base: :class:`~cryptoprice.asset.BaseAsset`
        :param quote: quote asset to get prices for
        :type quote: :class:`~cryptoprice.asset.BaseAsset`
        :return: URL
        :rtype: str
        """

        return self.SPOT_PRICE_URL.format(base.EXCHANGE_NAMES[self.NAME],
                                          quote.EXCHANGE_NAMES[self.NAME])

class ExchangeFactory(object):
    """Factory to return an exchange given its name"""

    # exchange class map
    EXCHANGES = {
        "kraken": Kraken,
        "localbitcoins": LocalBitcoins,
        "coinbase": Coinbase
    }

    @classmethod
    def from_str(cls, exchange_name, *args, **kwargs):
        """Returns exchange given its name

        :param exchange_name: exchange name
        :type exchange_name: str
        :return: exchange object
        :rtype: :class:`~cryptoprice.exchange.BaseExchange`
        :raises ValueError: if exchange name is unrecognised
        """

        exchange_name = exchange_name.lower()

        # check if exchange exists
        if exchange_name in cls.EXCHANGES.keys():
            return cls.EXCHANGES[exchange_name](*args, **kwargs)

        raise ValueError("Unrecognised exchange")

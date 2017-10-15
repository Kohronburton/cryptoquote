"""Crypto and fiat currency asset classes"""

import abc

class BaseAsset(object, metaclass=abc.ABCMeta):
    """Abstract class representing a crypto or fiat currency"""

    # asset name
    NAME = "NONE"

    # asset symbol (e.g. £)
    SYMBOL = "?"

    # format string for asset value
    VALUE_FORMAT_STR = "%f"

    # dict of names for this asset given by various exchanges
    EXCHANGE_NAMES = {}

    def exchange_name(self, exchange):
        """Returns the name of this asset as used by the specified exchange

        :param exchange: exchange name
        :type exchange: str
        :return: asset name at exchange
        :rtype: str
        """

        return self.EXCHANGE_NAMES[str(exchange)]

    def __str__(self):
        return self.NAME

    @property
    def value_prefix(self):
        """Assest value prefix"""

        # just return the symbol itself
        return self.SYMBOL

    def formatted_value(self, value):
        return ("%s" + self.VALUE_FORMAT_STR) % (self.value_prefix, value)

class UnknownAsset(BaseAsset):
    """Unknown asset"""

    NAME = "?"

    EXCHANGE_NAMES = {
        "Kraken": "?"
    }

class CryptoAsset(BaseAsset):
    """Abstract cryptocurrency asset"""

    @property
    def value_prefix(self):
        """Assest value prefix

        Overrides parent. Cryptocurrencies should have an extra space between
        the asset symbol and the value.
        """

        return "%s " % super(CryptoAsset, self).value_prefix

class BCHAsset(CryptoAsset):
    """Bitcoin Cash cryptocurrency"""

    NAME = "BCH"
    SYMBOL = "BCH"

    EXCHANGE_NAMES = {
        "Kraken": "BCH"
    }

class BTCAsset(CryptoAsset):
    """Bitcoin cryptocurrency"""

    NAME = "BTC"
    SYMBOL = "BTC"

    EXCHANGE_NAMES = {
        "Kraken": "XXBT"
    }

class DOGEAsset(CryptoAsset):
    """Dogecoin cryptocurrency"""

    NAME = "DOGE"
    SYMBOL = "Ð"

    EXCHANGE_NAMES = {
        "Kraken": "XXDG"
    }

class EOSAsset(CryptoAsset):
    """EOS cryptocurrency"""

    NAME = "EOS"
    SYMBOL = "EOS"

    EXCHANGE_NAMES = {
        "Kraken": "EOS"
    }

class ETHAsset(CryptoAsset):
    """Etherium cryptocurrency"""

    NAME = "ETH"
    SYMBOL = "ETH"

    EXCHANGE_NAMES = {
        "Kraken": "XETH"
    }

class GNOAsset(CryptoAsset):
    """Gnosis cryptocurrency"""

    NAME = "GNO"
    SYMBOL = "GNO"

    EXCHANGE_NAMES = {
        "Kraken": "GNO"
    }

class DASHAsset(CryptoAsset):
    """Dash cryptocurrency"""

    NAME = "DASH"
    SYMBOL = "DASH"

    EXCHANGE_NAMES = {
        "Kraken": "DASH"
    }

class FiatAsset(BaseAsset):
    """Abstract fiat currency asset"""

    # fiat currency values all have 2 decimal places
    VALUE_FORMAT_STR = "%.2f"

class EURAsset(FiatAsset):
    """Euro fiat currency"""

    NAME = "EUR"
    SYMBOL = "€"

    EXCHANGE_NAMES = {
        "Kraken": "ZEUR"
    }

class GBPAsset(FiatAsset):
    """British pound fiat currency"""

    NAME = "GBP"
    SYMBOL = "£"

    EXCHANGE_NAMES = {
        "Kraken": "ZGBP"
    }

class JPYAsset(FiatAsset):
    """Japanese yen fiat currency"""

    NAME = "JPY"
    SYMBOL = "¥"

    EXCHANGE_NAMES = {
        "Kraken": "ZEUR"
    }

class USDAsset(FiatAsset):
    """United States dollar fiat currency"""

    NAME = "USD"
    SYMBOL = "$"

    EXCHANGE_NAMES = {
        "Kraken": "ZUSD"
    }

class BaseAssetPair(object, metaclass=abc.ABCMeta):
    """Represents a pair of assets on an exchange"""

    # exchange name
    EXCHANGE = None

    def __init__(self, pair_name, pretty_name, base_asset, quote_asset):
        """Instantiates a new abstract asset pair

        :param pair_name: internal/API name of asset pair used by the exchange
        :type pair_name: str
        :param pretty_name: public name of asset pair
        :type pretty_name: str
        :param base_asset: base asset
        :type base_asset: :class:`~cryptoprice.asset.BaseAsset`
        :param quote_asset: quote asset
        :type quote_asset: :class:`~cryptoprice.asset.BaseAsset`
        """

        self.pair_name = str(pair_name)
        self.pretty_name = str(pretty_name)
        self.base_asset = base_asset
        self.quote_asset = quote_asset

    def __str__(self):
        return "%s (%s -> %s) on %s" % (self.asset_name,
                                        self.base_asset.exchange_name(self.EXCHANGE),
                                        self.quote_asset.exchange_name(self.EXCHANGE),
                                        self.EXCHANGE)

class KrakenAssetPair(BaseAssetPair):
    """Represents a pair of assets on Kraken"""

    EXCHANGE = "Kraken"

    def __init__(self, pair_name, asset_data):
        """Instantiates a new Kraken asset pair

        :param pair_name: internal/API name of asset pair used by Kraken
        :type pair_name: str
        :param asset_data: asset information provided by Kraken
        :type asset_data: dict
        """

        # extract asset information
        pair_name = str(pair_name)
        pretty_name = str(asset_data["altname"])
        base_asset = AssetFactory.from_str(asset_data["base"])
        quote_asset = AssetFactory.from_str(asset_data["quote"])

        # construct asset pair
        super(KrakenAssetPair, self).__init__(pair_name, pretty_name,
                                              base_asset, quote_asset)

    @property
    def quote_str(self):
        """Returns pair name used to obtain a quote

        :return: pair name
        :rtype: str
        """

        # pretty name is used by Kraken for quotes
        return self.pretty_name

class AssetFactory(object):
    """Factory to return an asset given its name or pretty name"""

    # asset class map
    ASSETS = {
        # crypto
        "BCH": BCHAsset,
        "EOS": EOSAsset,
        "ETH": ETHAsset,
        "XETH": ETHAsset,
        "DASH": DASHAsset,
        "DOGE": DOGEAsset,
        "XXDG": DOGEAsset,
        "GNO": GNOAsset,
        "XXBT": BTCAsset,
        # fiat
        "EUR": EURAsset,
        "ZEUR": EURAsset,
        "GBP": GBPAsset,
        "ZGBP": GBPAsset,
        "JPY": JPYAsset,
        "ZJPY": JPYAsset,
        "USD": USDAsset,
        "ZUSD": USDAsset,
    }

    @classmethod
    def from_str(cls, asset_name, *args, **kwargs):
        """Returns asset given its name

        :param asset_name: asset name
        :type asset_name: str
        """

        # check if asset exists
        if asset_name in cls.ASSETS.keys():
            return cls.ASSETS[asset_name](*args, **kwargs)
        else:
            # unknown asset
            return UnknownAsset()

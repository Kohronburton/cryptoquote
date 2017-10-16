import sys
import os
import io
import logging
import collections
import json
import argparse
import textwrap

from .exchange import ExchangeFactory
from .asset import AssetFactory
from .cache import delete_cache

PROG = "cq"
DESC = "Cryptocurrency quotes on the command line"

SYNOPSIS = "{} <command> [<args>...]".format(PROG)

MANPAGE = """
NAME
  {prog} - {desc}

SYNOPSIS
  {synopsis}

DESCRIPTION

  Command line tool to retrieve cryptocurrency quotes.

COMMANDS

{{cmds}}

AUTHOR
    Sean Leavey <cryptoprice@attackllama.com>
""".format(prog=PROG,
           desc=DESC,
           synopsis=SYNOPSIS,
           ).strip()

def enable_verbose_logs():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def get_exchange(exchange):
    return ExchangeFactory.from_str(exchange)

class Cmd(object):
    """Base class for commands"""

    cmd = ""

    def __init__(self):
        """Initialise argument parser"""

        self.parser = argparse.ArgumentParser(
            prog="{} {}".format(PROG, self.cmd),
            description=self.__doc__.strip(),
        )

    def parse_args(self, args):
        """Parse arguments and returned ArgumentParser Namespace object"""

        return self.parser.parse_args(args)

    def __call__(self, args):
        """Take Namespace object as input and execute command"""

        pass

class Price(Cmd):
    """Fetch asset price"""

    cmd = "price"

    def __init__(self):
        Cmd.__init__(self)

        self.parser.add_argument("base",
                                 help="base asset")
        self.parser.add_argument("quote",
                                 help="quote asset")
        self.parser.add_argument("-e", "--exchange", default="Kraken",
                                 help="exchange from which to fetch prices")
        self.parser.add_argument("-v", "--verbose", action="store_true",
                                 help="enable verbose output")

    def __call__(self, args):
        if args.verbose:
            enable_verbose_logs()

        # get exchange object
        exchange = get_exchange(args.exchange)

        try:
            quote = exchange.quote(args.base, args.quote)
        except ValueError as e:
            print("Specified base and quote assets are not available at this "
                  "exchange", file=sys.stderr)

            sys.exit(1)

        print(quote)

class List(Cmd):
    """List exchanges"""

    cmd = "list"

    def __init__(self):
        Cmd.__init__(self)

        self.parser.add_argument("type",
                                 help="object types to list, e.g. \"exchanges\" "
                                      "or \"assets\"")

    def __call__(self, args):
        obj = args.type.lower()

        if obj == "exchanges":
            exchanges = ExchangeFactory.EXCHANGES

            print("Supported exchanges:")
            for k in sorted(exchanges.keys()):
                print("\t%s (%s)" % (exchanges[k].NAME, exchanges[k].URL))
        elif obj == "assets":
            crypto_assets = AssetFactory.CRYPTO_ASSETS

            # running list of cryptocurrencies printed
            crypto_list = []

            print("Supported cryptocurrency assets:")
            for k in sorted(crypto_assets.keys()):
                asset = crypto_assets[k]

                if asset in crypto_list:
                    # don't print asset again
                    continue

                alt_names = ""

                if len(asset.ALT_NAMES):
                    alt_names = "(" + ", ".join(asset.ALT_NAMES) + ")"

                print("\t", asset.NAME, alt_names)

                # add currency to list of those printed
                crypto_list.append(asset)

            fiat_assets = AssetFactory.FIAT_ASSETS

            # running list of fiat currencies printed
            fiat_list = []

            print("Supported fiat currency assets:")
            for k in sorted(fiat_assets.keys()):
                asset = fiat_assets[k]

                if asset in fiat_list:
                    # don't print asset again
                    continue

                alt_names = ""

                if len(asset.ALT_NAMES):
                    alt_names = "(" + ", ".join(asset.ALT_NAMES) + ")"

                print("\t", asset.NAME, alt_names)

                # add currency to list of those printed
                fiat_list.append(asset)

class Reset(Cmd):
    """Reset cache"""

    cmd = "reset"

    def __init__(self):
        Cmd.__init__(self)

        self.parser.add_argument("-v", "--verbose", action="store_true",
                                 help="enable verbose output")

    def __call__(self, args):
        if args.verbose:
            enable_verbose_logs()

        delete_cache()

class Help(Cmd):
    """Print manpage or command help (also '-h' after command)"""

    cmd = "help"

    def __init__(self):
        Cmd.__init__(self)

        self.parser.add_argument("cmd", nargs="?",
                                 help="command")

    def __call__(self, args):
        if args.cmd:
            get_func(args.cmd).parser.print_help()
        else:
            print(MANPAGE.format(cmds=format_commands(man=True)))

CMDS = collections.OrderedDict([
    ("price", Price),
    ("list", List),
    ("reset", Reset),
    ("help", Help),
])

ALIAS = {
    "--help": "help",
    "-h": "help",
}

def format_commands(man=False):
    prefix = " " * 8

    wrapper = textwrap.TextWrapper(
        width=70,
        initial_indent=prefix,
        subsequent_indent=prefix,
        )

    with io.StringIO() as f:
        for name, func in CMDS.items():
            if man:
                fo = func()

                usage = fo.parser.format_usage()[len("usage: {} ".format(PROG)):].strip()
                desc = wrapper.fill('\n'.join([l.strip() for l in fo.parser.description.splitlines() if l]))

                f.write("  {}  \n".format(usage))
                f.write(desc + "\n")
                f.write("\n")
            else:
                desc = func.__doc__.splitlines()[0]
                f.write("  {:10}{}\n".format(name, desc))

        output = f.getvalue()

    return output.rstrip()

def get_func(cmd):
    if cmd in ALIAS:
        cmd = ALIAS[cmd]

    try:
        return CMDS[cmd]()
    except KeyError:
        print("Unknown command:", cmd, file=sys.stderr)
        print("See 'help' for usage.", file=sys.stderr)

        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Command not specified.", file=sys.stderr)
        print("usage: " + SYNOPSIS, file=sys.stderr)
        print(file=sys.stderr)
        print(format_commands(), file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    func = get_func(cmd)
    func(func.parse_args(args))

if __name__ == "__main__":
    main()

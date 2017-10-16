# Cryptoquote
Bitcoin, Etherium and other cryptocurrency quotes via the terminal using Kraken's API

## Prerequisites
  - Python 3
  - `requests`
  - `appdirs`

## Installation
Currently no installation available; run the script with:
```bash
$ cd /path/to/cryptoquote
$ python3 -m cryptoquote
```

## Usage
`Cryptoquote` has a command line interpreter. Call:
```bash
$ cq help
```
to get started.

### Quotes
For simple quote retrieval, call:
```bash
$ cq price <base> <quote>
```
where `<base>` is the base asset identifier (e.g. `BTC`) and `<quote>` is the
quote asset identifier (e.g. `USD`). For example, to get the current price of
bitcoin in US dollars, call:
```bash
$ cq price BTC USD
```
This will output something like:
```
BTC price on Kraken as of 16/10/17 10:41:56:
        Ask: $5607.50
        Bid: $5606.30
        Last: $5604.90
        Today low: $5550.00 (last 24h: $5462.10)
        Today high: $5708.10 (last 24h: $5731.28)
```
The date shown conforms to the user's locale.

### Available exchanges
Type `cq list exchanges` to get a list of supported exchanges. Currently only
Kraken is supported.

### Available assets
Type `cq list assets` to get a list of supported assets.

### Python module
`Cryptoquote` can also be imported as a Python 3 module.

# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2019

from __future__ import unicode_literals

import os
import sys
from datetime import datetime, timedelta

import dateutil.tz
import pkg_resources
import yaml
from colorama import Back, Fore


class Config(object):
    TZ_LOCAL = dateutil.tz.gettz("Europe/London")
    TZ_UTC = dateutil.tz.UTC

    BITTYTAX_PATH = os.path.expanduser("~/.bittytax")
    BITTYTAX_CONFIG = "bittytax.conf"
    CACHE_DIR = os.path.join(BITTYTAX_PATH, "cache")

    FIAT_LIST = ["GBP", "EUR", "USD"]
    CRYPTO_LIST = ["BTC", "ETH", "XRP", "LTC", "BCH", "USDT"]

    FORMAT_CSV = "CSV"
    FORMAT_EXCEL = "EXCEL"
    FORMAT_RECAP = "RECAP"

    TAX_RULES_UK_INDIVIDUAL = "UK_INDIVIDUAL"
    TAX_RULES_UK_COMPANY = [
        "UK_COMPANY_JAN",
        "UK_COMPANY_FEB",
        "UK_COMPANY_MAR",
        "UK_COMPANY_APR",
        "UK_COMPANY_MAY",
        "UK_COMPANY_JUN",
        "UK_COMPANY_JUL",
        "UK_COMPANY_AUG",
        "UK_COMPANY_SEP",
        "UK_COMPANY_OCT",
        "UK_COMPANY_NOV",
        "UK_COMPANY_DEC",
    ]

    TRADE_ASSET_TYPE_BUY = 0
    TRADE_ASSET_TYPE_SELL = 1
    TRADE_ASSET_TYPE_PRIORITY = 2

    TRADE_ALLOWABLE_COST_BUY = 0
    TRADE_ALLOWABLE_COST_SELL = 1
    TRADE_ALLOWABLE_COST_SPLIT = 2

    DATA_SOURCE_FIAT = ["BittyTaxAPI"]
    DATA_SOURCE_CRYPTO = ["CryptoCompare", "CoinGecko"]

    DEFAULT_CONFIG = {
        "local_currency": "GBP",
        "fiat_list": FIAT_LIST,
        "crypto_list": CRYPTO_LIST,
        "trade_asset_type": TRADE_ASSET_TYPE_PRIORITY,
        "trade_allowable_cost_type": TRADE_ALLOWABLE_COST_SPLIT,
        "audit_hide_empty": False,
        "show_empty_wallets": False,
        "transfers_include": False,
        "transfer_fee_disposal": True,
        "transfer_fee_allowable_cost": False,
        "fiat_income": False,
        "lost_buyback": True,
        "data_source_select": {},
        "data_source_fiat": DATA_SOURCE_FIAT,
        "data_source_crypto": DATA_SOURCE_CRYPTO,
        "usernames": [],
        "coinbase_zero_fees_are_gifts": False,
        "binance_multi_bnb_split_even": False,
    }

    def __init__(self):
        self.debug = False
        self.output = sys.stdout
        self.start_of_year_month = 4
        self.start_of_year_day = 6

        if not os.path.exists(Config.BITTYTAX_PATH):
            os.mkdir(Config.BITTYTAX_PATH)

        if not os.path.exists(os.path.join(Config.BITTYTAX_PATH, Config.BITTYTAX_CONFIG)):
            default_conf = pkg_resources.resource_string(
                __name__, "config/" + Config.BITTYTAX_CONFIG
            )
            with open(
                os.path.join(Config.BITTYTAX_PATH, Config.BITTYTAX_CONFIG), "wb"
            ) as config_file:
                config_file.write(default_conf)

        try:
            with open(
                os.path.join(Config.BITTYTAX_PATH, Config.BITTYTAX_CONFIG), "rb"
            ) as config_file:
                self.config = yaml.safe_load(config_file)
        except IOError:
            sys.stderr.write(
                "%sERROR%s Config file cannot be loaded: %s\n"
                % (
                    Back.RED + Fore.BLACK,
                    Back.RESET + Fore.RED,
                    os.path.join(Config.BITTYTAX_PATH, Config.BITTYTAX_CONFIG),
                )
            )
            sys.exit(1)
        except yaml.scanner.ScannerError as e:
            sys.stderr.write(
                "%sERROR%s Config file contains an error:\n%s\n"
                % (Back.RED + Fore.BLACK, Back.RESET + Fore.RED, e)
            )
            sys.exit(1)

        for name, default in self.DEFAULT_CONFIG.items():
            if name not in self.config:
                self.config[name] = default

        self.ccy = self.config["local_currency"]
        self.asset_priority = self.config["fiat_list"] + self.config["crypto_list"]

    def __getattr__(self, name):
        return self.config[name]

    def output_config(self):
        self.output.write(
            '%sconfig: "%s"\n'
            % (
                Fore.GREEN,
                os.path.join(Config.BITTYTAX_PATH, Config.BITTYTAX_CONFIG),
            )
        )

        for name in self.DEFAULT_CONFIG:
            self.output.write("%sconfig: %s: %s\n" % (Fore.GREEN, name, self.config[name]))

    def sym(self):
        if self.ccy == "GBP":
            return "\xA3"  # £
        if self.ccy == "EUR":
            return "\u20AC"  # €
        if self.ccy in ("USD", "AUD", "NZD"):
            return "$"
        if self.ccy in ("DKK", "NOK", "SEK"):
            return "kr."

        raise ValueError("Currency not supported")

    def get_tax_year_start(self, tax_year):
        if self.start_of_year_month != 1:
            return datetime(
                tax_year - 1,
                self.start_of_year_month,
                self.start_of_year_day,
                tzinfo=config.TZ_LOCAL,
            )
        return datetime(
            tax_year,
            self.start_of_year_month,
            self.start_of_year_day,
            tzinfo=config.TZ_LOCAL,
        )

    def get_tax_year_end(self, tax_year):
        if self.start_of_year_month == 1:
            return datetime(
                tax_year + 1,
                self.start_of_year_month,
                self.start_of_year_day,
                tzinfo=config.TZ_LOCAL,
            ) - timedelta(microseconds=1)
        return datetime(
            tax_year,
            self.start_of_year_month,
            self.start_of_year_day,
            tzinfo=config.TZ_LOCAL,
        ) - timedelta(microseconds=1)

    def format_tax_year(self, tax_year):
        start = self.get_tax_year_start(tax_year)
        end = self.get_tax_year_end(tax_year)

        if start.year == end.year:
            return start.strftime("%Y")
        return "{}/{}".format(start.strftime("%Y"), end.strftime("%y"))


config = Config()

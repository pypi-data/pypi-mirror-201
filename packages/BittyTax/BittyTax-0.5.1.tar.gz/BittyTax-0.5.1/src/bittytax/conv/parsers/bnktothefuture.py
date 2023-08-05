# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2022

import re
from decimal import Decimal

import yaml

from ..dataparser import DataParser
from ..exceptions import UnexpectedContentError, UnexpectedTypeError
from ..out_record import TransactionOutRecord

WALLET = "BnkToTheFuture"

ASSET_NORMALISE = {"USD*": "USD"}


def parse_bnktothefuture(data_row, parser, **_kwargs):
    row_dict = data_row.row_dict
    data_row.timestamp = DataParser.parse_timestamp(row_dict["Date"])

    if row_dict["Description"] in ("Dividend", "Deposit"):
        dtls = yaml.safe_load(row_dict["Details"])

        if "Related Company" in dtls:
            fee_quantity = None
            fee_asset = ""

            if 0 in dtls:
                fee_quantity = str(dtls[0]["Amount"])
                fee_asset = _asset(dtls[0]["Currency"])

            data_row.t_record = TransactionOutRecord(
                TransactionOutRecord.TYPE_DIVIDEND,
                data_row.timestamp,
                buy_quantity=row_dict["In"],
                buy_asset=_asset(row_dict["Currency"]),
                fee_quantity=fee_quantity,
                fee_asset=fee_asset,
                wallet=WALLET,
                note=dtls["Related Company"]["Name"],
            )
        else:
            data_row.t_record = TransactionOutRecord(
                TransactionOutRecord.TYPE_DEPOSIT,
                data_row.timestamp,
                buy_quantity=row_dict["In"],
                buy_asset=_asset(row_dict["Currency"]),
                wallet=WALLET,
            )
    elif row_dict["Description"] == "Reward":
        data_row.t_record = TransactionOutRecord(
            TransactionOutRecord.TYPE_GIFT_RECEIVED,
            data_row.timestamp,
            buy_quantity=row_dict["In"],
            buy_asset=_asset(row_dict["Currency"]),
            wallet=WALLET,
        )

    elif row_dict["Description"] == "Outcome Transaction":
        dtls = yaml.safe_load(row_dict["Details"])

        if "Related Crypto Trade" in dtls:
            data_row.t_record = TransactionOutRecord(
                TransactionOutRecord.TYPE_TRADE,
                data_row.timestamp,
                buy_quantity=str(dtls["Related Crypto Trade"]["Income Amount"]),
                buy_asset=_asset(dtls["Related Crypto Trade"]["Income Currency"]),
                sell_quantity=row_dict["Out"],
                sell_asset=_asset(row_dict["Currency"]),
                fee_quantity=str(dtls["Related Crypto Trade"]["Fee"]),
                fee_asset=_asset(row_dict["Currency"]),
                wallet=WALLET,
            )
        else:
            raise UnexpectedContentError(
                parser.in_header.index("Details"), "Details", row_dict["Details"]
            )

    elif row_dict["Description"] == "Withdrawal":
        fee_quantity = None
        fee_asset = ""

        # Kludge to fix invalid yaml
        yaml_fix = re.sub(r"^.*?Related transaction:", "", row_dict["Details"])
        if yaml_fix:
            dtls = yaml.safe_load(yaml_fix)
            for rel_tx in dtls:
                if dtls[rel_tx]["Description"] == "Fee":
                    fee_quantity = str(dtls[rel_tx]["Amount"])
                    fee_asset = _asset(dtls[rel_tx]["Currency"])
                    break

        data_row.t_record = TransactionOutRecord(
            TransactionOutRecord.TYPE_WITHDRAWAL,
            data_row.timestamp,
            sell_quantity=row_dict["Out"],
            sell_asset=_asset(row_dict["Currency"]),
            fee_quantity=fee_quantity,
            fee_asset=fee_asset,
            wallet=WALLET,
        )
    elif row_dict["Description"] == "Fee":
        dtls = yaml.safe_load(row_dict["Details"])
        if 0 in dtls and dtls[0]["Description"] in ("Dividend", "Withdrawal"):
            # Skip as fee already included
            return

        if "Related Crypto Trade" in dtls:
            # Skip as fee already included
            return

        data_row.t_record = TransactionOutRecord(
            TransactionOutRecord.TYPE_SPEND,
            data_row.timestamp,
            sell_quantity=Decimal(0),
            sell_asset=_asset(row_dict["Currency"]),
            fee_quantity=row_dict["Out"],
            fee_asset=_asset(row_dict["Currency"]),
            wallet=WALLET,
        )
    elif row_dict["Description"] in (
        "Pending Transaction/Order",
        "Funds Released",
        "Income Transaction",
    ):
        # Skip internal operations
        return
    else:
        raise UnexpectedTypeError(
            parser.in_header.index("Description"),
            "Description",
            row_dict["Description"],
        )


def _asset(local_asset):
    if local_asset in ASSET_NORMALISE:
        return local_asset.replace(local_asset, ASSET_NORMALISE[local_asset]).upper()
    return local_asset.upper()


DataParser(
    DataParser.TYPE_SAVINGS,
    "BnkToTheFuture",
    ["Date", "Description", "Currency", "Details", "Transaction ID", "In", "Out"],
    worksheet_name="BnkToTheFuture",
    row_handler=parse_bnktothefuture,
)

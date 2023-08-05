import csv
import pathlib

import pendulum

from housenomics.transaction import Transaction


def transaction_from_source(transaction):
    row_columns = transaction[0].split(";")

    # Date
    date = row_columns[0].split("-")
    date.reverse()
    date = pendulum.parse("-".join(date))

    # Find the value of the transaction
    unit = row_columns[3].replace(".", "")
    decimals = transaction[1].split(";")[0]

    # Find if it is a credit or a debit
    is_credit = False
    if not unit:
        is_credit = True
        unit = row_columns[4].replace(".", "")

    # Get the value of the transaction
    value: float = 0
    if is_credit:
        value = float(f"{unit}.{decimals}")
    if not is_credit:
        value = -1 * float(f"{unit}.{decimals}")

    # Create the actual transaction
    m = Transaction(
        description=row_columns[2],
        date_of_movement=date,
        value=value,
        origin="CGD",
    )
    return m


class GatewayCGD:
    def __init__(self, csv_file_path: pathlib.Path):
        self.csv_file_path = csv_file_path
        self.read_obj = None

    def __iter__(self):
        self.read_obj = open(self.csv_file_path, "r", encoding="ISO-8859-1")
        self.csv_reader = csv.reader(self.read_obj)

        return _Converter(self.csv_reader)

    def __del__(self):
        if self.read_obj is not None:
            self.read_obj.close()


class _Converter:
    def __init__(self, csv_reader):
        self._reader = csv_reader

        # Ignore the headers of the file
        number_of_headers = 7
        for i in range(number_of_headers):
            next(self._reader)

    def __next__(self):
        value = next(self._reader)

        # Ignore last lines of the file
        # TODO: is this being used ??
        if value[0].split(";")[0] == "('":
            raise StopIteration

        # Ignore last lines of the file
        if "Saldo conta" in value[0]:
            raise StopIteration

        t = transaction_from_source(value)

        return t

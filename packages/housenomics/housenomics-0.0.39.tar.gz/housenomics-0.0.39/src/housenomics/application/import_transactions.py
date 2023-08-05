class ServiceImportTransactions:
    def __init__(self, source_transactions, transactions):
        self._source_transactions = source_transactions
        self._transactions = transactions

    def execute(self):
        for transaction in self._source_transactions:
            self._transactions.append(transaction)

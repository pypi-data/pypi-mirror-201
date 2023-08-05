from housenomics.transaction import Transaction


class Transactions:
    def __init__(self, session):
        self.session = session

    def append(self, t: Transaction):
        self.session.add(t)

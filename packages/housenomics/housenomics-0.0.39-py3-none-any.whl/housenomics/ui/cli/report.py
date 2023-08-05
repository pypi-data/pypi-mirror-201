from sqlalchemy.orm import Session

from housenomics.application.views.transactions import ViewTransactions
from toolbox.database import Database


def report(database_path, seller, since, on):
    with Session(Database(database_path).engine) as session:
        view = ViewTransactions(session, seller, since, on)

    transactions, total = view.data
    if not seller:
        if not transactions:
            print("Could not find any transactions!")
            return

        for t in transactions:
            print(f"Description: '{t['description']:>22}', Value: {t['value']:>10}")
        return

    print(f"Description: '{seller}', Value: {round(total, 2)}")

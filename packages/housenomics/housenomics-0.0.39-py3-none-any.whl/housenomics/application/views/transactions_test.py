import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from housenomics.application.views.transactions import ViewTransactions
from housenomics.transaction import (  # noqa because is used to create the database
    Transaction,
)
from toolbox.database import Database


@pytest.fixture
def tmp_db_session(tmp_path):
    """
    Crates a database in the path define by tmpdir.
    """

    db = Database(tmp_path)

    with Session(db.engine) as session:
        pass

    with Session(db.engine) as session:
        yield session


@pytest.mark.integration
def test_shown_no_transactions_on_empty_database(tmp_db_session):
    transactions, total = ViewTransactions(tmp_db_session).data

    assert not transactions  # nosec
    assert not total  # nosec


class Scenario:
    def __init__(self, session):
        self.session = session

    def with_transaction(self, description, value, date_of_movement, origin):
        sql_statement = """
            INSERT INTO 'transaction' (description, value, date_of_movement, origin)
                 VALUES (:description, :value, :date_of_movement, :origin)
        """

        prepared_statement = text(sql_statement).bindparams(
            description=description,
            value=value,
            date_of_movement=date_of_movement,
            origin=origin,
        )

        self.session.execute(prepared_statement)
        return self


@pytest.mark.integration
def test_show_one_transaction_when_one_is_available(tmp_db_session):
    """
    Given a database with one transaction
    When the view is executed
    Then the transaction is shown
    """

    scenario = Scenario(tmp_db_session)
    scenario = scenario.with_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session).data

    assert transactions == [{"description": "foo", "value": 1}]  # nosec
    assert total == 1  # nosec


@pytest.mark.integration
def test_show_multiple_transactions_when_more_than_one_is_available(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed
    Then the transactions are shown
    """

    scenario = Scenario(tmp_db_session)
    scenario = scenario.with_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.with_transaction(
        description="bar", value=2, date_of_movement="2020-01-01", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session).data

    assert transactions == [  # nosec
        {"description": "foo", "value": 1},
        {"description": "bar", "value": 2},
    ]
    assert total == 3  # nosec


@pytest.mark.integration
def test_show_transactions_since_a_given_date(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed with a since date
    Then the transactions since the given date are shown
    """

    scenario = Scenario(tmp_db_session)
    scenario = scenario.with_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.with_transaction(
        description="bar", value=2, date_of_movement="2020-01-02", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session, since="2020-01-02").data

    assert transactions == [{"description": "bar", "value": 2}]  # nosec
    assert total == 2  # nosec


@pytest.mark.integration
def test_show_transactions_on_a_given_date(tmp_db_session):
    """
    Given a database with multiple transactions
    When the view is executed with a on date
    Then the transactions on the given date are shown
    """

    scenario = Scenario(tmp_db_session)
    scenario = scenario.with_transaction(
        description="foo", value=1, date_of_movement="2020-01-01", origin="foo"
    )
    scenario = scenario.with_transaction(
        description="bar", value=2, date_of_movement="2020-01-02", origin="foo"
    )

    transactions, total = ViewTransactions(tmp_db_session, on="2020-01-01").data

    assert transactions == [{"description": "foo", "value": 1.0}]  # nosec
    assert total == 1.0  # nosec

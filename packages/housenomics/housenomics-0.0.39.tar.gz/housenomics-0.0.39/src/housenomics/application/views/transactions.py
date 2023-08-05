import typing

from sqlalchemy import text

from toolbox.views import View


class DatabaseSessioner(typing.Protocol):
    def scalars(*_):
        pass


class ViewTransactions(View):
    def __init__(
        self, session: DatabaseSessioner, seller=None, since=None, on=None
    ) -> None:
        self._seller = seller
        self._session = session
        self._since = since
        self._on = on

    @property
    def data(self):
        """
        The data resulting from the view execution.
        """

        # Construct the query
        sql_stmt = "SELECT description, value FROM 'transaction'"
        if self._since:
            sql_stmt += " WHERE date_of_movement >= :since"
        if self._on:
            sql_stmt += " WHERE date_of_movement = :on"

        # Bind parameters
        prepared_statement = text(sql_stmt)
        if self._since:
            prepared_statement = prepared_statement.bindparams(since=self._since)
        if self._on:
            prepared_statement = prepared_statement.bindparams(on=self._on)

        rows = self._session.execute(prepared_statement)

        data = []
        for row in rows:
            data.append(
                {
                    "description": row[0],
                    "value": row[1],
                }
            )

        total: float = 0
        for movement in data:
            if not self._seller:
                total += float(movement["value"])  # type: ignore
                continue

            if (
                self._seller
                and self._seller.lower() in str(movement["description"]).lower()
            ):
                total += float(movement["value"])  # type: ignore

        return data, total

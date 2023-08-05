import os
import pathlib
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    """
    Creates a database in the path defined by the DATABASE environment variable.
    If the environment variable is not defined, it will create a database in the
    path defined by the database_path parameter.
    """

    def __init__(self, database_path: Optional[pathlib.Path] = None) -> None:
        """
        param: database_name: Path to where the database file will be created.
        """

        # Get the database path from the environment variable
        # The environment variable always has priority over the definition
        # defined by the application.
        try:
            env_path = os.environ["DATABASE"]
        except KeyError:
            # It can happen the environment variable does not exist, but the
            # database path was defined by the application.
            if not database_path:
                raise KeyError("Please set the DATABASE environment variable.")
        else:
            if env_path:
                database_path = pathlib.Path(env_path)

        # Create the database directory
        database_path.mkdir(parents=True, exist_ok=True)  # type: ignore

        # Discover the database file location
        self._database_file = str(database_path / "database.db")  # type: ignore
        sqlite_url = f"sqlite:///{self._database_file}"

        # Create the database engine
        engine = create_engine(sqlite_url, echo=False)
        Base.metadata.create_all(engine)
        self.engine = engine

    def remove(self):
        pathlib.Path(self._database_file).unlink(missing_ok=True)

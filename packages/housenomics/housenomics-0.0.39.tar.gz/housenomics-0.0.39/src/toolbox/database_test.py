import pytest

from toolbox.database import Database


def test_should_raise_a_key_error_when_environment_variable_is_not_defined(monkeypatch):
    monkeypatch.delenv("DATABASE")
    with pytest.raises(KeyError):
        _ = Database()


def test_create_database_file_in_default_directory_when_database_env_variable_is_undefined(
    tmpdir,
):
    _ = Database()

    assert tmpdir.join("database.db").exists()  # nosec


def test_create_database_file_in_path_defined_by_environment_variable(
    tmpdir, monkeypatch
):
    database = tmpdir / "database_file_by_env.db"

    monkeypatch.setenv("DATABASE", str(database))

    _ = Database()

    assert database.exists()  # nosec


def test_remove_the_database_file_when_remove_is_called(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE")

    database = tmp_path / "database.db"

    db = Database(tmp_path)

    assert database.exists()  # nosec

    db.remove()

    assert not database.exists()  # nosec

import pytest
from unittest.mock import patch, MagicMock
from src.database import (
    create_tables,
    save_location,
    get_location,
    get_all_users,
    delete_location
)


@pytest.fixture
def in_memory_db(tmp_path):
    """Fixture – tworzy tymczasową bazę danych dla każdego testu."""
    test_db = tmp_path / "test.db"

    with patch('src.database.DB_PATH', test_db):
        create_tables()
        yield test_db


def test_create_tables(in_memory_db):
    """Test tworzenia tabel."""
    # Tabele powinny być utworzone bez błędu
    assert in_memory_db.exists()


def test_save_location(in_memory_db):
    """Test zapisywania lokalizacji."""
    with patch('src.database.DB_PATH', in_memory_db):
        result = save_location("user_123", 52.23, 21.01, "Warszawa")

    assert result == True


def test_get_location(in_memory_db):
    """Test pobierania lokalizacji."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")

        location = get_location("user_123")

    assert location is not None
    lat, lon, city = location
    assert lat == pytest.approx(52.23, abs=0.01)
    assert lon == pytest.approx(21.01, abs=0.01)
    assert city == "Warszawa"


def test_get_location_not_found(in_memory_db):
    """Test pobierania lokalizacji – użytkownik nie istnieje."""
    with patch('src.database.DB_PATH', in_memory_db):
        location = get_location("nonexistent_user")

    assert location is None


def test_save_location_update(in_memory_db):
    """Test aktualizacji lokalizacji (ten sam user_id)."""
    with patch('src.database.DB_PATH', in_memory_db):
        # Zapisz Warszawa
        save_location("user_123", 52.23, 21.01, "Warszawa")

        # Update na Gdańsk
        save_location("user_123", 54.35, 18.65, "Gdańsk")

        # Sprawdź czy zaktualizowano
        location = get_location("user_123")

    assert location is not None
    lat, lon, city = location
    assert city == "Gdańsk"
    assert lat == pytest.approx(54.35, abs=0.01)


def test_get_all_users(in_memory_db):
    """Test pobierania wszystkich użytkowników."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")
        save_location("user_456", 50.06, 19.94, "Kraków")

        users = get_all_users()

    assert len(users) == 2


def test_delete_location(in_memory_db):
    """Test usuwania lokalizacji."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")

        # Usuń
        result = delete_location("user_123")
        assert result == True

        # Sprawdź czy usunięto
        location = get_location("user_123")
        assert location is None


def test_save_location_error():
    """Test zapisu z błędem bazy danych."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = save_location("user_123", 52.23, 21.01, "Warszawa")

    assert result == False


def test_get_location_error():
    """Test pobierania z błędem bazy danych."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = get_location("user_123")

    assert result is None


def test_get_all_users_error():
    """Test pobierania wszystkich z błędem bazy danych."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = get_all_users()

    assert result == []


def test_delete_location_error():
    """Test usuwania z błędem bazy danych."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = delete_location("user_123")

    assert result == False
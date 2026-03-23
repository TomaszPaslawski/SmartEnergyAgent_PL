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
    """Fixture – creates temporary database for each test."""
    test_db = tmp_path / "test.db"

    with patch('src.database.DB_PATH', test_db):
        create_tables()
        yield test_db


def test_create_tables(in_memory_db):
    """Test - tables creation."""
    # Tables created without errors
    assert in_memory_db.exists()


def test_save_location(in_memory_db):
    """Test - saving location."""
    with patch('src.database.DB_PATH', in_memory_db):
        result = save_location("user_123", 52.23, 21.01, "Warszawa")

    assert result == True


def test_get_location(in_memory_db):
    """Test - reading location."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")

        location = get_location("user_123")

    assert location is not None
    lat, lon, city = location
    assert lat == pytest.approx(52.23, abs=0.01)
    assert lon == pytest.approx(21.01, abs=0.01)
    assert city == "Warszawa"


def test_get_location_not_found(in_memory_db):
    """Test - reading location, user does not exist."""
    with patch('src.database.DB_PATH', in_memory_db):
        location = get_location("nonexistent_user")

    assert location is None


def test_save_location_update(in_memory_db):
    """Test - updating location (same user_id)."""
    with patch('src.database.DB_PATH', in_memory_db):
        # Save Warszawa
        save_location("user_123", 52.23, 21.01, "Warszawa")

        # Update to Gdańsk
        save_location("user_123", 54.35, 18.65, "Gdańsk")

        # Check if updated
        location = get_location("user_123")

    assert location is not None
    lat, lon, city = location
    assert city == "Gdańsk"
    assert lat == pytest.approx(54.35, abs=0.01)


def test_get_all_users(in_memory_db):
    """Test - reading all users."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")
        save_location("user_456", 50.06, 19.94, "Kraków")

        users = get_all_users()

    assert len(users) == 2


def test_delete_location(in_memory_db):
    """Test - location removal."""
    with patch('src.database.DB_PATH', in_memory_db):
        save_location("user_123", 52.23, 21.01, "Warszawa")

        # Delete
        result = delete_location("user_123")
        assert result == True

        # Check if removed
        location = get_location("user_123")
        assert location is None


def test_save_location_error():
    """Test - saving with errors."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = save_location("user_123", 52.23, 21.01, "Warszawa")

    assert result == False


def test_get_location_error():
    """Test - reading with error."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = get_location("user_123")

    assert result is None


def test_get_all_users_error():
    """Test - reading all users with error."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = get_all_users()

    assert result == []


def test_delete_location_error():
    """Test - removal with error."""
    with patch('src.database.get_db_connection') as mock_conn:
        mock_conn.side_effect = Exception("DB error")

        result = delete_location("user_123")

    assert result == False
import sqlite3
from typing import Optional, Tuple, List
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "smartenergy.db"


def get_db_connection() -> sqlite3.Connection:
    """
    Creates connections with SQLite.

    Returns:
        sqlite3.Connection: Object connected with the database
    """
    # Ensure that data folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows access to columns by name
    return conn


def create_tables():
    """
    Creates table in the database (if does not exist).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users' locations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_locations (
            user_id TEXT PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            city_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    logger.info(f"Tables created in: {DB_PATH}")


def save_location(user_id: str, latitude: float, longitude: float, city_name: str) -> bool:
    """
    Saves user's location to database.
    If user already exists, it will be updated.

    Args:
        user_id (str): User's unique ID (e.g. Telegram user_id)
        latitude (float): latitude
        longitude (float): longitude
        city_name (str): City

    Returns:
        bool: True if success, False if error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # INSERT or REPLACE (upsert)
        cursor.execute("""
            INSERT INTO user_locations (user_id, latitude, longitude, city_name, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                latitude = excluded.latitude,
                longitude = excluded.longitude,
                city_name = excluded.city_name,
                updated_at = excluded.updated_at
        """, (user_id, latitude, longitude, city_name, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        logger.info(f"Location has been saved for user_id={user_id}: {city_name} ({latitude:.2f}, {longitude:.2f})")
        return True

    except Exception as e:
        logger.error(f"Error during saving location: {e}")
        return False


def get_location(user_id: str) -> Optional[Tuple[float, float, str]]:
    """
    Reads user's location from database.

    Args:
        user_id (str): Unique user's ID

    Returns:
        Optional[Tuple[float, float, str]]:
            - (latitude, longitude, city_name) if founded
            - None if user does not have saved location
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT latitude, longitude, city_name
            FROM user_locations
            WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return (row['latitude'], row['longitude'], row['city_name'])
        else:
            logger.warning(f"No locations saved for user_id={user_id}")
            return None

    except Exception as e:
        logger.error(f"Error during location reading: {e}")
        return None


def get_all_users() -> List[Tuple[str, float, float, str]]:
    """
    Reads all users from database.

    Returns:
        List[Tuple[str, float, float, str]]:
            List (user_id, latitude, longitude, city_name)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, latitude, longitude, city_name
            FROM user_locations
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [(row['user_id'], row['latitude'], row['longitude'], row['city_name'])
                for row in rows]

    except Exception as e:
        logger.error(f"Error during users' reading: {e}")
        return []


def delete_location(user_id: str) -> bool:
    """
    Removes user's location from database.

    Args:
        user_id (str): User's unique ID

    Returns:
        bool: True - location removed, False - error during removal
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user_locations WHERE user_id = ?", (user_id,))

        conn.commit()
        conn.close()

        logger.info(f"Location has been removed for user_id={user_id}")
        return True

    except Exception as e:
        logger.error(f"Error during location removal: {e}")
        return False


# Test section
if __name__ == "__main__":
    print("\n--- Test database.py ---")

    # Test 1: Tables creation
    print("\n1. Creating table...")
    create_tables()
    print(f"   ✅ Database created: {DB_PATH}")

    # Test 2: Saving location
    print("\n2. Saving location...")
    success = save_location("user_123", 52.2297, 21.0122, "Warszawa")
    print(f"   {'✅' if success else '❌'} Saved user_123")

    success = save_location("user_456", 50.0647, 19.9450, "Kraków")
    print(f"   {'✅' if success else '❌'} Saved user_456")

    # Test 3: Reading location
    print("\n3. Reading location...")
    location = get_location("user_123")
    if location:
        lat, lon, city = location
        print(f"   ✅ user_123: {city} ({lat:.2f}°N, {lon:.2f}°E)")
    else:
        print("   ❌ Location not found")

    # Test 4: Update (same user_id)
    print("\n4. Updating location...")
    success = save_location("user_123", 54.3520, 18.6466, "Gdańsk")
    print(f"   {'✅' if success else '❌'} Updated user_123")

    location = get_location("user_123")
    if location:
        lat, lon, city = location
        print(f"   ✅ user_123 (po update): {city} ({lat:.2f}°N, {lon:.2f}°E)")

    # Test 5: Reading all users data
    print("\n5. Reading all users data...")
    users = get_all_users()
    print(f"   Found {len(users)} users:")
    for user_id, lat, lon, city in users:
        print(f"   - {user_id}: {city} ({lat:.2f}°N, {lon:.2f}°E)")

    # Test 6: Removal
    print("\n6. Removing location...")
    success = delete_location("user_456")
    print(f"   {'✅' if success else '❌'} Removed user_456")

    users = get_all_users()
    print(f"   Remains {len(users)} users")

    print("\n--- Tests completed ---")
    print(f"\nDatabase: {DB_PATH.absolute()}")
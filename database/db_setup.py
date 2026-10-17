import sqlite3
from pathlib import Path

# Project ke database folder ka path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "database" / "nabha.db"


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. User health profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            age INTEGER CHECK (age IS NULL OR age > 0),
            health_condition TEXT DEFAULT 'None',
            profession TEXT,
            outdoor_exposure TEXT,
            FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    # 3. Historical and live AQI records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_history (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            recorded_at TEXT NOT NULL,
            aqi REAL,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            so2 REAL,
            co REAL,
            o3 REAL
        )
    """)

    # 4. Next-day AQI predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            predicted_for TEXT NOT NULL,
            predicted_aqi REAL,
            model_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 5. Personalized health advisories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_advisories (
            advisory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            prediction_id INTEGER,
            risk_score INTEGER NOT NULL
                CHECK (risk_score BETWEEN 0 AND 100),
            risk_level TEXT NOT NULL,
            recommendations TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (prediction_id)
                REFERENCES predictions(prediction_id)
                ON DELETE SET NULL
        )
    """)

    conn.commit()

    # Verify database tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    print("NABHA DATABASE CREATED SUCCESSFULLY!")
    print("Database location:", DB_PATH)
    print("\nTables created:")

    for row in cursor.fetchall():
        print("-", row[0])

    conn.close()


if __name__ == "__main__":
    create_database()
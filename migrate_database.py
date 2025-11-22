"""
Database migration script - Run this to update your existing database with new columns
"""

import sqlite3
from config import DATABASE_PATH

def migrate_database():
    """Add missing columns to existing reminders table"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Check if columns exist
            cursor.execute("PRAGMA table_info(reminders)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Add missing columns
            if 'is_recurring' not in columns:
                cursor.execute('ALTER TABLE reminders ADD COLUMN is_recurring INTEGER DEFAULT 0')
                print("✓ Added 'is_recurring' column")
            
            if 'recurrence_type' not in columns:
                cursor.execute('ALTER TABLE reminders ADD COLUMN recurrence_type TEXT')
                print("✓ Added 'recurrence_type' column")
            
            conn.commit()
            print("\n✓ Database migration completed successfully!")
            print("You can now run: python main.py\n")
            
    except Exception as e:
        print(f"✗ Migration error: {e}")
        print("\nIf you're still getting errors, try:")
        print("1. Delete the 'data' folder")
        print("2. Run: python main.py")
        print("\nThis will create a fresh database.\n")

if __name__ == "__main__":
    migrate_database()

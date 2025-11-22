"""
Database management for reminders
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from config import DATABASE_PATH

class ReminderDatabase:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    category TEXT DEFAULT 'General',
                    priority TEXT DEFAULT 'Normal',
                    is_completed INTEGER DEFAULT 0,
                    is_recurring INTEGER DEFAULT 0,
                    recurrence_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_reminder(self, title, description, date, time, category, priority, is_recurring=0, recurrence_type=None):
        """Add a new reminder"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO reminders 
                    (title, description, date, time, category, priority, is_recurring, recurrence_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, description, date, time, category, priority, is_recurring, recurrence_type))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return None
    
    def get_reminders_by_date(self, date):
        """Get all reminders for a specific date"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM reminders 
                    WHERE date = ? 
                    ORDER BY time ASC
                ''', (date,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching reminders: {e}")
            return []
    
    def get_all_reminders(self):
        """Get all reminders"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM reminders 
                    ORDER BY date DESC, time ASC
                ''')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching reminders: {e}")
            return []
    
    def update_reminder(self, reminder_id, title, description, date, time, category, priority, is_recurring=0, recurrence_type=None):
        """Update an existing reminder"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE reminders 
                    SET title = ?, description = ?, date = ?, time = ?, 
                        category = ?, priority = ?, is_recurring = ?, recurrence_type = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (title, description, date, time, category, priority, is_recurring, recurrence_type, reminder_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating reminder: {e}")
            return False
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting reminder: {e}")
            return False
    
    def mark_completed(self, reminder_id, is_completed):
        """Mark reminder as completed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE reminders 
                    SET is_completed = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (int(is_completed), reminder_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error marking reminder: {e}")
            return False
    
    def get_reminders_by_category(self, category):
        """Get reminders by category"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM reminders 
                    WHERE category = ? 
                    ORDER BY date DESC, time ASC
                ''', (category,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching reminders by category: {e}")
            return []
    
    def get_reminders_by_priority(self, priority):
        """Get reminders by priority"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM reminders 
                    WHERE priority = ? 
                    ORDER BY date DESC, time ASC
                ''', (priority,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching reminders by priority: {e}")
            return []
    
    def search_reminders(self, query):
        """Search reminders by title or description"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM reminders 
                    WHERE title LIKE ? OR description LIKE ?
                    ORDER BY date DESC, time ASC
                ''', (f"%{query}%", f"%{query}%"))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error searching reminders: {e}")
            return []

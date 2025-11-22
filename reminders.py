"""
Reminder management logic
"""

from datetime import datetime, timedelta
from database import ReminderDatabase

class ReminderManager:
    def __init__(self):
        self.db = ReminderDatabase()
        self.categories = ["Work", "Personal", "Health", "Shopping", "General"]
        self.priorities = ["Low", "Normal", "High", "Urgent"]
        self.recurrence_types = ["Daily", "Weekly", "Monthly"]
    
    def create_reminder(self, title, description, date, time, category, priority, is_recurring=0, recurrence_type=None):
        """Create a new reminder"""
        if not self._validate_reminder(title, date, time):
            return False
        
        reminder_id = self.db.add_reminder(title, description, date, time, category, priority, is_recurring, recurrence_type)
        return reminder_id is not None
    
    def _validate_reminder(self, title, date, time):
        """Validate reminder inputs"""
        if not title or not title.strip():
            return False
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
            return True
        except ValueError:
            return False
    
    def get_upcoming_reminders(self, days=7):
        """Get reminders for the next N days"""
        reminders = self.db.get_all_reminders()
        upcoming = []
        
        today = datetime.now()
        cutoff_date = today + timedelta(days=days)
        
        for reminder in reminders:
            if not reminder['is_completed']:
                reminder_date = datetime.strptime(reminder['date'], "%Y-%m-%d")
                if today <= reminder_date <= cutoff_date:
                    upcoming.append(reminder)
        
        return upcoming
    
    def get_today_reminders(self):
        """Get today's reminders"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_reminders_by_date(today)
    
    def get_overdue_reminders(self):
        """Get overdue reminders"""
        all_reminders = self.db.get_all_reminders()
        overdue = []
        today = datetime.now()
        
        for reminder in all_reminders:
            if not reminder['is_completed']:
                reminder_date = datetime.strptime(reminder['date'], "%Y-%m-%d")
                if reminder_date < today:
                    overdue.append(reminder)
        
        return overdue
    
    def complete_reminder(self, reminder_id):
        """Mark reminder as completed"""
        return self.db.mark_completed(reminder_id, True)
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        return self.db.delete_reminder(reminder_id)
    
    def get_statistics(self):
        """Get reminder statistics"""
        all_reminders = self.db.get_all_reminders()
        
        stats = {
            "total": len(all_reminders),
            "completed": len([r for r in all_reminders if r['is_completed']]),
            "pending": len([r for r in all_reminders if not r['is_completed']]),
            "overdue": len(self.get_overdue_reminders()),
        }
        
        return stats

"""
Notification and alert system with sound support
"""

import platform
import os
from datetime import datetime

class NotificationManager:
    def __init__(self):
        self.system = platform.system()
    
    def show_notification(self, title, message):
        """Show system notification"""
        try:
            if self.system == "Darwin":  # macOS
                self._notify_macos(title, message)
            elif self.system == "Windows":
                self._notify_windows(title, message)
            elif self.system == "Linux":
                self._notify_linux(title, message)
        except Exception as e:
            print(f"Notification error: {e}")
    
    def _notify_windows(self, title, message):
        """Windows notification"""
        try:
            # Use Windows 10+ notification
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=10, threaded=True)
        except ImportError:
            # Fallback
            print(f"NOTIFICATION: {title}")
            print(f"MESSAGE: {message}")
    
    def _notify_macos(self, title, message):
        """macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            os.system(f'osascript -e \'{script}\'')
        except Exception as e:
            print(f"NOTIFICATION: {title}\nMESSAGE: {message}")
    
    def _notify_linux(self, title, message):
        """Linux notification"""
        try:
            import subprocess
            subprocess.run(["notify-send", title, message], check=True)
        except Exception:
            print(f"NOTIFICATION: {title}\nMESSAGE: {message}")
    
    def play_alert_sound(self):
        """Enhanced sound alerts for Windows with winsound module"""
        try:
            if self.system == "Windows":
                import winsound
                # Play dual beep for alert
                winsound.Beep(1500, 300)  # High frequency, 300ms
                winsound.Beep(1000, 300)  # Lower frequency, 300ms
            elif self.system == "Darwin":
                os.system('afplay /System/Library/Sounds/Alarm.aiff')
            elif self.system == "Linux":
                os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || speaker-test -t sine -f 1000 -l 1')
        except Exception as e:
            print(f"Sound playback: {e}")
    
    def alert_reminder(self, reminder):
        """Enhanced alert with sound and system notifications"""
        title = f"Reminder: {reminder['title']}"
        message = f"Time: {reminder['time']}\nCategory: {reminder['category']}\nPriority: {reminder['priority']}"
        
        # Show notification
        self.show_notification(title, message)
        
        # Play sound alert
        self.play_alert_sound()
        
        # Also print to console for debugging
        print(f"\n{'='*50}")
        print(f"REMINDER ALERT!")
        print(f"Title: {reminder['title']}")
        print(f"Time: {reminder['time']}")
        print(f"Category: {reminder['category']}")
        print(f"Priority: {reminder['priority']}")
        print(f"Description: {reminder.get('description', 'N/A')}")
        print(f"{'='*50}\n")
    
    def format_time(self, time_str):
        """Format time string"""
        try:
            time_obj = datetime.strptime(time_str, "%H:%M")
            return time_obj.strftime("%I:%M %p")
        except:
            return time_str

"""
Configuration settings for Calendar & Reminder App
"""

import os
from pathlib import Path

# App Settings
APP_NAME = "Calendar & Reminder Manager"
APP_VERSION = "2.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Database
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "reminders.db"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Professional Color Palette (Modern Light Theme)
COLORS = {
    # Primary colors
    "primary": "#0066FF",          # Bright blue
    "primary_dark": "#0052CC",     # Darker blue
    "primary_light": "#E3F2FF",    # Light blue
    
    # Secondary colors
    "secondary": "#1F2937",        # Dark gray
    "secondary_light": "#F3F4F6",  # Light gray
    
    # Semantic colors
    "success": "#10B981",          # Green
    "warning": "#F59E0B",          # Amber
    "danger": "#EF4444",           # Red
    "info": "#3B82F6",             # Blue
    
    # UI colors
    "background": "#FFFFFF",       # White background
    "surface": "#F9FAFB",          # Light surface
    "surface_alt": "#F3F4F6",      # Alternative surface
    "border": "#E5E7EB",           # Border color
    "border_dark": "#D1D5DB",      # Darker border
    
    # Text colors
    "text_primary": "#111827",     # Almost black
    "text_secondary": "#6B7280",   # Gray
    "text_tertiary": "#9CA3AF",    # Light gray
    "text_inverse": "#FFFFFF",     # White
    
    # Calendar specific
    "today": "#FEF3C7",            # Light yellow
    "selected": "#0066FF",         # Primary blue
    "weekend": "#F3F4F6",          # Light background
    "hover": "#E3F2FF",            # Light blue
    
    # Header
    "header_bg": "#FFFFFF",        # White header
    "header_border": "#E5E7EB",    # Subtle border
    "header_text": "#111827",      # Dark text
    
    # Accent
    "accent": "#FF6B6B",           # Coral red
    "accent_dark": "#DC2626",      # Dark red
}

FONT_FAMILY = "Segoe UI"
FONT_HEADING = (FONT_FAMILY, 24, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
FONT_LABEL = (FONT_FAMILY, 11, "normal")
FONT_SMALL = (FONT_FAMILY, 9, "normal")

# UI Settings
BUTTON_COLOR = COLORS["primary"]
BUTTON_HOVER_COLOR = COLORS["primary_dark"]
BUTTON_TEXT_COLOR = COLORS["text_inverse"]

HEADER_BG = COLORS["header_bg"]
HEADER_FG = COLORS["header_text"]

CALENDAR_BG = COLORS["background"]
CALENDAR_GRID_COLOR = COLORS["border"]
CALENDAR_SELECTED_COLOR = COLORS["selected"]
CALENDAR_TODAY_COLOR = COLORS["today"]

REMINDER_BG = COLORS["surface"]
REMINDER_BORDER = COLORS["border"]

# Reminder Settings
REMINDER_SOUND_ENABLED = True
REMINDER_NOTIFICATION_ENABLED = True
REMINDER_CHECK_INTERVAL = 60000  # milliseconds (check every minute)

# Category Colors
CATEGORY_COLORS = {
    "Work": "#0066FF",
    "Personal": "#8B5CF6",
    "Health": "#EF4444",
    "Shopping": "#F59E0B",
    "General": "#06B6D4",
}

# Priority Colors
PRIORITY_COLORS = {
    "Low": "#10B981",
    "Normal": "#3B82F6",
    "High": "#F59E0B",
    "Urgent": "#EF4444",
}

# Calendar Grid sizing
CALENDAR_CELL_WIDTH = 15
CALENDAR_CELL_HEIGHT = 8

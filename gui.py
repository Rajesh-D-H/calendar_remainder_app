"""
GUI Interface for Calendar and Reminder App - Professional Modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from calendar import monthcalendar, month_name
from datetime import datetime, timedelta
from reminders import ReminderManager
from notifications import NotificationManager
from config import *

class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1200, 750)
        self.root.configure(bg=COLORS["background"])
        
        self.reminder_manager = ReminderManager()
        self.notification_manager = NotificationManager()
        
        self.current_date = datetime.now()
        self.selected_date = None
        self.selected_reminder_id = None
        
        self.setup_styles()
        self.create_widgets()
        self.update_calendar()
        self.check_reminders()
    
    def setup_styles(self):
        """Configure professional UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=COLORS["background"])
        style.configure('TLabel', background=COLORS["background"], foreground=COLORS["text_primary"])
        style.configure('TButton', background=COLORS["primary"], foreground=COLORS["text_inverse"])
        style.configure('TNotebook', background=COLORS["background"])
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Custom styles
        style.configure('Header.TLabel', font=FONT_HEADING, foreground=COLORS["header_text"])
        style.configure('Title.TLabel', font=FONT_SUBHEADING, foreground=COLORS["text_primary"])
        style.configure('Normal.TLabel', font=FONT_LABEL, foreground=COLORS["text_secondary"])
        style.configure('Small.TLabel', font=FONT_SMALL, foreground=COLORS["text_tertiary"])
        
        style.configure('Primary.TButton', font=FONT_LABEL)
        style.map('Primary.TButton',
                 background=[('active', COLORS["primary_dark"]),
                            ('pressed', COLORS["primary_dark"])])
        
        style.configure('TCombobox', fieldbackground=COLORS["background"])
    
    def create_widgets(self):
        """Create main UI structure with modern layout"""
        # Header bar
        self.create_header_bar()
        
        # Main content area with sidebar
        main_container = tk.Frame(self.root, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar for calendar
        sidebar = tk.Frame(main_container, bg=COLORS["background"], width=400, relief=tk.FLAT)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=15, pady=15)
        sidebar.pack_propagate(False)
        
        self.create_calendar_section(sidebar)
        
        # Main content area
        content = tk.Frame(main_container, bg=COLORS["background"])
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Today & Selected Date
        today_tab = ttk.Frame(self.notebook)
        self.notebook.add(today_tab, text="Dashboard")
        self.create_dashboard_tab(today_tab)
        
        # Tab 2: All Reminders
        reminders_tab = ttk.Frame(self.notebook)
        self.notebook.add(reminders_tab, text="All Reminders")
        self.create_all_reminders_tab(reminders_tab)
        
        # Tab 3: Filters
        filters_tab = ttk.Frame(self.notebook)
        self.notebook.add(filters_tab, text="Smart Filters")
        self.create_filters_tab(filters_tab)
    
    def create_header_bar(self):
        """Create professional header bar"""
        header = tk.Frame(self.root, bg=COLORS["header_bg"], height=80, relief=tk.FLAT)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=COLORS["header_bg"])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left side - Title
        left_frame = tk.Frame(header_content, bg=COLORS["header_bg"])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(left_frame, text="📅 " + APP_NAME, 
                              bg=COLORS["header_bg"], fg=COLORS["header_text"],
                              font=FONT_HEADING)
        title_label.pack(side=tk.LEFT)
        
        # Right side - Statistics
        right_frame = tk.Frame(header_content, bg=COLORS["header_bg"])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.stats_label = tk.Label(right_frame, 
                                   bg=COLORS["header_bg"], 
                                   fg=COLORS["text_secondary"],
                                   font=FONT_LABEL)
        self.stats_label.pack(side=tk.RIGHT)
        
        self.update_statistics()
        
        # Bottom border
        border = tk.Frame(header, bg=COLORS["header_border"], height=1)
        border.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_calendar_section(self, parent):
        """Create calendar section in sidebar with improved layout"""
        # Month navigation
        nav_frame = tk.Frame(parent, bg=COLORS["background"])
        nav_frame.pack(fill=tk.X, pady=(0, 15))
        
        nav_buttons = tk.Frame(nav_frame, bg=COLORS["background"])
        nav_buttons.pack(fill=tk.X)
        
        ttk.Button(nav_buttons, text="◄ Prev", command=self.prev_month, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_buttons, text="Today", command=self.go_to_today, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_buttons, text="Next ►", command=self.next_month, width=8).pack(side=tk.LEFT, padx=2)
        
        self.month_label = tk.Label(nav_frame, text="", 
                                   bg=COLORS["background"],
                                   fg=COLORS["text_primary"],
                                   font=FONT_SUBHEADING)
        self.month_label.pack(fill=tk.X, pady=(10, 0))
        
        # Calendar grid with proper spacing
        calendar_container = tk.Frame(parent, bg=COLORS["surface"], relief=tk.FLAT, highlightthickness=1, 
                                     highlightbackground=COLORS["border"])
        calendar_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            is_weekend = i >= 5
            day_label = tk.Label(calendar_container, text=day,
                               bg=COLORS["weekend"] if is_weekend else COLORS["surface"],
                               fg=COLORS["text_primary"],
                               font=(FONT_LABEL[0], FONT_LABEL[1], "bold"),
                               pady=8)
            day_label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Date cells
        self.date_buttons = {}
        for row in range(1, 7):
            for col in range(7):
                btn = tk.Button(calendar_container, text="",
                              command=lambda r=row, c=col: self.select_date(r, c),
                              bg=COLORS["background"], 
                              fg=COLORS["text_primary"],
                              relief=tk.FLAT,
                              font=FONT_LABEL,
                              padx=0, pady=10,
                              activebackground=COLORS["hover"],
                              activeforeground=COLORS["text_primary"],
                              highlightthickness=0,
                              bd=0)
                btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
                self.date_buttons[(row, col)] = btn
        
        # Configure grid weights for equal sizing
        for i in range(7):
            calendar_container.grid_columnconfigure(i, weight=1)
        for i in range(7):
            calendar_container.grid_rowconfigure(i, weight=1)
        
        # Selected date info
        info_frame = tk.Frame(parent, bg=COLORS["surface"], relief=tk.FLAT, highlightthickness=1,
                             highlightbackground=COLORS["border"])
        info_frame.pack(fill=tk.X)
        
        self.selected_date_label = tk.Label(info_frame, text="Select a date",
                                           bg=COLORS["surface"],
                                           fg=COLORS["text_primary"],
                                           font=FONT_LABEL,
                                           pady=8)
        self.selected_date_label.pack(fill=tk.X, padx=10, pady=10)
    
    def create_dashboard_tab(self, parent):
        """Create dashboard tab showing selected date and today's reminders"""
        main_frame = tk.Frame(parent, bg=COLORS["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Today's Reminders Section
        today_section = self.create_card(main_frame, "Today's Reminders")
        today_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.today_listbox = tk.Listbox(today_section, height=8, width=60,
                                       bg=COLORS["surface"],
                                       fg=COLORS["text_primary"],
                                       font=FONT_SMALL,
                                       selectmode=tk.SINGLE,
                                       relief=tk.FLAT,
                                       bd=0,
                                       highlightthickness=0)
        self.today_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.today_listbox.bind("<<ListboxSelect>>", self.on_reminder_select)
        
        # Selected Date Reminders Section
        selected_section = self.create_card(main_frame, "Selected Date Reminders")
        selected_section.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.date_reminders_listbox = tk.Listbox(selected_section, height=8, width=60,
                                                bg=COLORS["surface"],
                                                fg=COLORS["text_primary"],
                                                font=FONT_SMALL,
                                                selectmode=tk.SINGLE,
                                                relief=tk.FLAT,
                                                bd=0,
                                                highlightthickness=0)
        self.date_reminders_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.date_reminders_listbox.bind("<<ListboxSelect>>", self.on_reminder_select)
        
        # Action buttons
        actions = tk.Frame(main_frame, bg=COLORS["background"])
        actions.pack(fill=tk.X)
        
        ttk.Button(actions, text="+ Add Reminder", command=self.add_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="✎ Edit", command=self.edit_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="✓ Mark Done", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="✕ Delete", command=self.delete_reminder).pack(side=tk.LEFT, padx=5)
    
    def create_all_reminders_tab(self, parent):
        """Create tab showing all reminders"""
        main_frame = tk.Frame(parent, bg=COLORS["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        card = self.create_card(main_frame, "All Reminders")
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Listbox with better styling
        self.all_reminders_listbox = tk.Listbox(card, height=20, width=80,
                                               bg=COLORS["surface"],
                                               fg=COLORS["text_primary"],
                                               font=FONT_SMALL,
                                               selectmode=tk.SINGLE,
                                               relief=tk.FLAT,
                                               bd=0,
                                               highlightthickness=0)
        self.all_reminders_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.all_reminders_listbox.bind("<<ListboxSelect>>", self.on_reminder_select)
        
        # Control buttons
        controls = tk.Frame(main_frame, bg=COLORS["background"])
        controls.pack(fill=tk.X)
        
        ttk.Button(controls, text="+ Add", command=self.add_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Refresh", command=self.refresh_all_reminders).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="✎ Edit", command=self.edit_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="✓ Done", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="✕ Delete", command=self.delete_reminder).pack(side=tk.LEFT, padx=5)
    
    def create_filters_tab(self, parent):
        """Create smart filters tab"""
        main_frame = tk.Frame(parent, bg=COLORS["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        filter_card = self.create_card(main_frame, "Filter Options")
        filter_card.pack(fill=tk.X, pady=(0, 15))
        
        filter_content = tk.Frame(filter_card, bg=COLORS["surface"])
        filter_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Quick filters
        quick_label = tk.Label(filter_content, text="Quick Filters:", 
                              bg=COLORS["surface"], fg=COLORS["text_primary"],
                              font=(FONT_LABEL[0], FONT_LABEL[1], "bold"))
        quick_label.pack(anchor=tk.W, pady=(0, 10))
        
        quick_buttons = tk.Frame(filter_content, bg=COLORS["surface"])
        quick_buttons.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(quick_buttons, text="Today", 
                  command=self.show_today_reminders).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_buttons, text="Overdue", 
                  command=self.show_overdue_reminders).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_buttons, text="Next 7 Days", 
                  command=self.show_upcoming_reminders).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_buttons, text="All", 
                  command=self.refresh_all_reminders).pack(side=tk.LEFT, padx=2)
        
        # Advanced filters
        advanced_label = tk.Label(filter_content, text="Advanced Filters:", 
                                 bg=COLORS["surface"], fg=COLORS["text_primary"],
                                 font=(FONT_LABEL[0], FONT_LABEL[1], "bold"))
        advanced_label.pack(anchor=tk.W, pady=(15, 10))
        
        filter_row = tk.Frame(filter_content, bg=COLORS["surface"])
        filter_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_row, text="Category:", bg=COLORS["surface"],
                fg=COLORS["text_secondary"], font=FONT_LABEL).pack(side=tk.LEFT, padx=(0, 5))
        self.category_filter = ttk.Combobox(filter_row, values=self.reminder_manager.categories,
                                           state='readonly', width=15)
        self.category_filter.pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_row, text="Filter", 
                  command=self.filter_by_category).pack(side=tk.LEFT, padx=5)
        
        priority_row = tk.Frame(filter_content, bg=COLORS["surface"])
        priority_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(priority_row, text="Priority:", bg=COLORS["surface"],
                fg=COLORS["text_secondary"], font=FONT_LABEL).pack(side=tk.LEFT, padx=(0, 5))
        self.priority_filter = ttk.Combobox(priority_row, values=self.reminder_manager.priorities,
                                           state='readonly', width=15)
        self.priority_filter.pack(side=tk.LEFT, padx=2)
        ttk.Button(priority_row, text="Filter", 
                  command=self.filter_by_priority).pack(side=tk.LEFT, padx=5)
        
        search_row = tk.Frame(filter_content, bg=COLORS["surface"])
        search_row.pack(fill=tk.X)
        
        tk.Label(search_row, text="Search:", bg=COLORS["surface"],
                fg=COLORS["text_secondary"], font=FONT_LABEL).pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_row, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(search_row, text="Search", 
                  command=self.search_reminders).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_card = self.create_card(main_frame, "Filter Results")
        results_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.filter_results_listbox = tk.Listbox(results_card, height=15, width=80,
                                                bg=COLORS["surface"],
                                                fg=COLORS["text_primary"],
                                                font=FONT_SMALL,
                                                selectmode=tk.SINGLE,
                                                relief=tk.FLAT,
                                                bd=0,
                                                highlightthickness=0)
        self.filter_results_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.filter_results_listbox.bind("<<ListboxSelect>>", self.on_reminder_select)
    
    def create_card(self, parent, title):
        """Create a modern card component"""
        card = tk.Frame(parent, bg=COLORS["surface"], relief=tk.FLAT, highlightthickness=1,
                       highlightbackground=COLORS["border"])
        
        # Title
        title_label = tk.Label(card, text=title, bg=COLORS["surface"],
                              fg=COLORS["text_primary"],
                              font=(FONT_LABEL[0], FONT_LABEL[1], "bold"),
                              pady=10, padx=15)
        title_label.pack(fill=tk.X, side=tk.TOP)
        
        # Divider
        divider = tk.Frame(card, bg=COLORS["border"], height=1)
        divider.pack(fill=tk.X, side=tk.TOP)
        
        return card
    
    def update_calendar(self):
        """Update calendar display with modern styling"""
        year = self.current_date.year
        month = self.current_date.month
        
        self.month_label.config(text=f"{month_name[month]} {year}")
        
        cal = monthcalendar(year, month)
        today = datetime.now().date()
        
        # Clear all buttons
        for btn in self.date_buttons.values():
            btn.config(text="", state=tk.DISABLED, bg=COLORS["background"])
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day > 0:
                    btn = self.date_buttons[(week_num + 1, day_num)]
                    btn.config(text=str(day), state=tk.NORMAL)
                    
                    date_obj = datetime(year, month, day).date()
                    is_weekend = day_num >= 5
                    
                    # Color logic
                    if date_obj == today:
                        btn.config(bg=COLORS["today"], fg=COLORS["text_primary"])
                    elif self.selected_date and self.selected_date == date_obj:
                        btn.config(bg=COLORS["selected"], fg=COLORS["text_inverse"])
                    elif is_weekend:
                        btn.config(bg=COLORS["weekend"], fg=COLORS["text_secondary"])
                    else:
                        btn.config(bg=COLORS["background"], fg=COLORS["text_primary"])
                    
                    btn.config(command=lambda d=day: self.select_date_by_day(d))
    
    def select_date(self, row, col):
        pass
    
    def select_date_by_day(self, day):
        """Select a date and update reminders display"""
        self.selected_date = datetime(self.current_date.year, self.current_date.month, day).date()
        self.update_calendar()
        self.selected_date_label.config(text=f"Selected: {self.selected_date.strftime('%A, %B %d, %Y')}")
        self.refresh_date_reminders()
    
    def prev_month(self):
        """Previous month"""
        first_day = self.current_date.replace(day=1)
        self.current_date = first_day - timedelta(days=1)
        self.update_calendar()
    
    def next_month(self):
        """Next month"""
        first_day = self.current_date.replace(day=1)
        self.current_date = first_day + timedelta(days=32)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()
    
    def go_to_today(self):
        """Go to today"""
        self.current_date = datetime.now()
        self.selected_date = datetime.now().date()
        self.update_calendar()
        self.selected_date_label.config(text=f"Today: {self.selected_date.strftime('%A, %B %d, %Y')}")
        self.refresh_date_reminders()
        self.refresh_today_reminders()
    
    def refresh_date_reminders(self):
        """Refresh selected date reminders"""
        self.date_reminders_listbox.delete(0, tk.END)
        
        if self.selected_date:
            date_str = self.selected_date.strftime("%Y-%m-%d")
            reminders = self.reminder_manager.db.get_reminders_by_date(date_str)
            
            if reminders:
                for reminder in reminders:
                    self.date_reminders_listbox.insert(tk.END, self.format_reminder_display(reminder))
            else:
                self.date_reminders_listbox.insert(tk.END, "No reminders for this date")
    
    def refresh_today_reminders(self):
        """Refresh today's reminders"""
        self.today_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.get_today_reminders()
        
        if reminders:
            for reminder in reminders:
                self.today_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.today_listbox.insert(tk.END, "No reminders for today")
    
    def refresh_all_reminders(self):
        """Refresh all reminders display"""
        self.all_reminders_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.db.get_all_reminders()
        
        if reminders:
            for reminder in reminders:
                self.all_reminders_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.all_reminders_listbox.insert(tk.END, "No reminders found")
    
    def format_reminder_display(self, reminder):
        """Format reminder for display"""
        status = "✓ DONE" if reminder['is_completed'] else "⏳ PENDING"
        priority_icon = {"Low": "●", "Normal": "●●", "High": "●●●", "Urgent": "●●●●"}
        recurring = " (↻)" if reminder.get('is_recurring') else ""
        
        return f"{reminder['time']} | {reminder['title'][:35]} | {status} | {priority_icon.get(reminder['priority'], '')} {reminder['category']}{recurring} (ID:{reminder['id']})"
    
    def on_reminder_select(self, event):
        """Handle reminder selection"""
        try:
            widget = event.widget
            index = widget.curselection()[0]
            selected_text = widget.get(index)
            self.extract_id_from_text(selected_text)
        except:
            pass
    
    def extract_id_from_text(self, text):
        """Extract reminder ID from display text"""
        try:
            if "ID:" in text:
                id_part = text.split("ID:")[1].strip(")")
                self.selected_reminder_id = int(id_part)
        except:
            pass
    
    def add_reminder(self):
        """Add new reminder"""
        dialog = ReminderDialog(self.root, self.reminder_manager)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_date_reminders()
            self.refresh_today_reminders()
            self.refresh_all_reminders()
            self.update_statistics()
    
    def edit_reminder(self):
        """Edit selected reminder"""
        if not self.selected_reminder_id:
            messagebox.showwarning("Warning", "Please select a reminder to edit")
            return
        
        all_reminders = self.reminder_manager.db.get_all_reminders()
        reminder = next((r for r in all_reminders if r['id'] == self.selected_reminder_id), None)
        
        if reminder:
            dialog = ReminderDialog(self.root, self.reminder_manager, reminder)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                self.refresh_date_reminders()
                self.refresh_today_reminders()
                self.refresh_all_reminders()
                self.update_statistics()
            
            self.selected_reminder_id = None
    
    def delete_reminder(self):
        """Delete selected reminder"""
        if not self.selected_reminder_id:
            messagebox.showwarning("Warning", "Please select a reminder to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reminder?"):
            self.reminder_manager.delete_reminder(self.selected_reminder_id)
            self.refresh_date_reminders()
            self.refresh_today_reminders()
            self.refresh_all_reminders()
            self.update_statistics()
            self.selected_reminder_id = None
    
    def mark_done(self):
        """Mark reminder as done"""
        if not self.selected_reminder_id:
            messagebox.showwarning("Warning", "Please select a reminder to mark as done")
            return
        
        self.reminder_manager.complete_reminder(self.selected_reminder_id)
        self.refresh_date_reminders()
        self.refresh_today_reminders()
        self.refresh_all_reminders()
        self.update_statistics()
        self.selected_reminder_id = None
    
    def show_today_reminders(self):
        """Show today's reminders"""
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.get_today_reminders()
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, "No reminders for today")
    
    def show_overdue_reminders(self):
        """Show overdue reminders"""
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.get_overdue_reminders()
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, "No overdue reminders")
    
    def show_upcoming_reminders(self):
        """Show upcoming reminders"""
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.get_upcoming_reminders(7)
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, "No upcoming reminders")
    
    def filter_by_category(self):
        """Filter by category"""
        category = self.category_filter.get()
        if not category:
            messagebox.showwarning("Warning", "Please select a category")
            return
        
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.db.get_reminders_by_category(category)
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, f"No reminders in '{category}'")
    
    def filter_by_priority(self):
        """Filter by priority"""
        priority = self.priority_filter.get()
        if not priority:
            messagebox.showwarning("Warning", "Please select a priority")
            return
        
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.db.get_reminders_by_priority(priority)
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, f"No reminders with priority '{priority}'")
    
    def search_reminders(self):
        """Search reminders"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        self.filter_results_listbox.delete(0, tk.END)
        reminders = self.reminder_manager.db.search_reminders(query)
        
        if reminders:
            for reminder in reminders:
                self.filter_results_listbox.insert(tk.END, self.format_reminder_display(reminder))
        else:
            self.filter_results_listbox.insert(tk.END, f"No reminders found matching '{query}'")
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.reminder_manager.get_statistics()
        text = f"Total: {stats['total']}  |  Pending: {stats['pending']}  |  Done: {stats['completed']}  |  Overdue: {stats['overdue']}"
        self.stats_label.config(text=text)
    
    def check_reminders(self):
        """Check for reminders that need to be notified"""
        try:
            self.refresh_today_reminders()
        except:
            pass
        
        now = datetime.now()
        today_reminders = self.reminder_manager.get_today_reminders()
        
        for reminder in today_reminders:
            if not reminder['is_completed']:
                try:
                    reminder_time = datetime.strptime(reminder['time'], "%H:%M")
                    current_time = now.replace(second=0, microsecond=0)
                    reminder_datetime = reminder_time.replace(
                        year=now.year, month=now.month, day=now.day
                    )
                    
                    if reminder_datetime == current_time:
                        self.notification_manager.alert_reminder(reminder)
                        messagebox.showinfo("Reminder Alert!", f"{reminder['title']}\nTime: {reminder['time']}\nCategory: {reminder['category']}")
                except Exception as e:
                    print(f"Error checking reminder: {e}")
        
        # Schedule next check
        self.root.after(REMINDER_CHECK_INTERVAL, self.check_reminders)


class ReminderDialog:
    def __init__(self, parent, reminder_manager, reminder=None):
        self.reminder_manager = reminder_manager
        self.result = False
        self.reminder_id = reminder['id'] if reminder else None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Reminder" if not reminder else "Edit Reminder")
        self.dialog.geometry("650x600")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLORS["background"])
        
        self.create_form(reminder)
    
    def create_form(self, reminder):
        """Create form with modern styling"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="Title:", font=FONT_SUBHEADING).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=50, font=FONT_LABEL)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 15))
        
        if reminder:
            self.title_entry.insert(0, reminder['title'])
        
        # Description
        ttk.Label(main_frame, text="Description:", font=FONT_SUBHEADING).grid(row=1, column=0, sticky=tk.NW, pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=4, width=50, font=FONT_LABEL,
                                       bg=COLORS["surface"], fg=COLORS["text_primary"],
                                       relief=tk.FLAT, bd=1, highlightthickness=1,
                                       highlightcolor=COLORS["border"])
        self.description_text.grid(row=1, column=1, sticky=tk.EW, pady=(0, 15))
        
        if reminder:
            self.description_text.insert(1.0, reminder['description'] or "")
        
        # Date
        ttk.Label(main_frame, text="Date (YYYY-MM-DD):", font=FONT_SUBHEADING).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.date_entry = ttk.Entry(main_frame, width=20, font=FONT_LABEL)
        self.date_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 15))
        
        if reminder:
            self.date_entry.insert(0, reminder['date'])
        else:
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time
        ttk.Label(main_frame, text="Time (HH:MM):", font=FONT_SUBHEADING).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.time_entry = ttk.Entry(main_frame, width=20, font=FONT_LABEL)
        self.time_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, 15))
        
        if reminder:
            self.time_entry.insert(0, reminder['time'])
        else:
            self.time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        # Category
        ttk.Label(main_frame, text="Category:", font=FONT_SUBHEADING).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.category_var = tk.StringVar(value=reminder['category'] if reminder else "General")
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var,
                                     values=self.reminder_manager.categories, state='readonly', width=47)
        category_combo.grid(row=4, column=1, sticky=tk.EW, pady=(0, 15))
        
        # Priority
        ttk.Label(main_frame, text="Priority:", font=FONT_SUBHEADING).grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar(value=reminder['priority'] if reminder else "Normal")
        priority_combo = ttk.Combobox(main_frame, textvariable=self.priority_var,
                                     values=self.reminder_manager.priorities, state='readonly', width=47)
        priority_combo.grid(row=5, column=1, sticky=tk.EW, pady=(0, 15))
        
        # Recurring
        self.recurring_var = tk.BooleanVar(value=reminder['is_recurring'] if reminder else False)
        recurring_check = ttk.Checkbutton(main_frame, text="This is a recurring reminder",
                                         variable=self.recurring_var)
        recurring_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Recurrence type
        ttk.Label(main_frame, text="Recurrence Type:", font=FONT_SUBHEADING).grid(row=7, column=0, sticky=tk.W, pady=(0, 5))
        self.recurrence_type_var = tk.StringVar(value=reminder['recurrence_type'] if reminder else "Daily")
        recurrence_combo = ttk.Combobox(main_frame, textvariable=self.recurrence_type_var,
                                       values=self.reminder_manager.recurrence_types, state='readonly', width=47)
        recurrence_combo.grid(row=7, column=1, sticky=tk.EW, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS["background"])
        button_frame.grid(row=8, column=0, columnspan=2, sticky=tk.E, pady=(15, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_reminder).pack(side=tk.LEFT, padx=5)
    
    def save_reminder(self):
        """Save reminder with validation"""
        title = self.title_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        is_recurring = 1 if self.recurring_var.get() else 0
        recurrence_type = self.recurrence_type_var.get() if is_recurring else None
        
        # Validation
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format\nUse YYYY-MM-DD for date and HH:MM for time")
            return
        
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        
        if self.reminder_id:
            self.reminder_manager.db.update_reminder(
                self.reminder_id, title, description, date, time, category, priority, is_recurring, recurrence_type
            )
        else:
            self.reminder_manager.create_reminder(
                title, description, date, time, category, priority, is_recurring, recurrence_type
            )
        
        self.result = True
        self.dialog.destroy()


def main():
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

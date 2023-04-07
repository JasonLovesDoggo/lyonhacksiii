import sqlite3
from datetime import datetime


class ReminderDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('reminders.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders
            (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, due_date TIMESTAMP)
        ''')
        self.conn.commit()

    def add_reminder(self, title, due_date):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO reminders (title, due_date) VALUES (?, ?)', (title, due_date))
        self.conn.commit()

    def get_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders ORDER BY due_date DESC')
        rows = cursor.fetchall()
        reminders = [{'id': row[0], 'title': row[1], 'due_date': datetime.fromisoformat(row[2])} for row in rows]
        return reminders

    def delete_reminder(self, reminder_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
        self.conn.commit()

    def update_reminder(self, reminder_id, title, due_date):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE reminders SET title = ?, due_date = ? WHERE id = ?', (title, due_date, reminder_id))
        self.conn.commit()

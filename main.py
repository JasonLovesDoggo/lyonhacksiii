from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import datetime

from utils.database import Database


class ReminderItem(TwoLineListItem):
    def __init__(self, title, due_date, **kwargs):
        super(ReminderItem, self).__init__(**kwargs)
        self.text = title
        self.secondary_text = due_date.strftime('%Y-%m-%d %H:%M:%S')


class RemindersApp(MDApp):
    def __init__(self, **kwargs):
        super(RemindersApp, self).__init__(**kwargs)
        self.db = Database()
        self.reminders = [
            {'title': 'Buy milk', 'due_date': datetime(2023, 4, 10, 10, 0, 0)},
            {'title': 'Pick up laundry', 'due_date': datetime(2023, 4, 12, 14, 0, 0)}
        ]

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.list = MDList()
        layout.add_widget(self.list)
        return layout

    def on_start(self):
        for reminder in self.reminders:
            self.list.add_widget(ReminderItem(title=reminder['title'], due_date=reminder['due_date']))

    def add_reminder(self, title, due_date):
        self.reminders.append({'title': title, 'due_date': due_date})
        self.list.add_widget(ReminderItem(title=title, due_date=due_date))

    def show_add_reminder_dialog(self):
        dialog = MDDialog(
            title='Add Reminder',
            type='custom',
            content_cls=ReminderDialogContent(add_reminder_callback=self.add_reminder)
        )
        dialog.open()


class ReminderDialogContent(BoxLayout):
    def __init__(self, add_reminder_callback, **kwargs):
        super(ReminderDialogContent, self).__init__(**kwargs)
        self.add_reminder_callback = add_reminder_callback

    def add_reminder(self):
        title = self.ids.title.text
        due_date_str = self.ids.due_date.text
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
        self.add_reminder_callback(title, due_date)


if __name__ == '__main__':
    RemindersApp().run()

from one_block.accessory import Accessory
from one_block.base import BasePlainText


class DatePicker(Accessory):
    def __init__(self, action_id, initial_date=None, placeholder=None):
        self.action_id = action_id
        self.initial_date = initial_date
        if placeholder:
            self.placeholder = BasePlainText(placeholder)
        else:
            self.placeholder = None

    def json(self):
        base = {
            'type': 'datepicker',
            'action_id': self.action_id
        }
        if self.initial_date:
            base['initial_date'] = self.initial_date
        if self.placeholder:
            base['placeholder'] = self.placeholder.json()
        return base


class TimePicker(Accessory):
    def __init__(self, action_id, initial_time=None, placeholder=None):
        self.action_id = action_id
        self.initial_time = initial_time
        if placeholder:
            self.placeholder = BasePlainText(placeholder)
        else:
            self.placeholder = None

    def json(self):
        base = {
            'type': 'timepicker',
            'action_id': self.action_id
        }
        if self.initial_time:
            base['initial_time'] = self.initial_time
        if self.placeholder:
            base['placeholder'] = self.placeholder.json()
        return base

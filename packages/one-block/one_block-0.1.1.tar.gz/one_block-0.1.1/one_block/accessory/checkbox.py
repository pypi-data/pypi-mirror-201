from one_block.accessory import Accessory


class Checkbox(Accessory):
    def __init__(self, action_id, options):
        self.action_id = action_id
        self.options = options

    def json(self):
        return {
            'type': 'checkboxes',
            'options': [
                option.json() for option in self.options
            ],
            'action_id': self.action_id
        }

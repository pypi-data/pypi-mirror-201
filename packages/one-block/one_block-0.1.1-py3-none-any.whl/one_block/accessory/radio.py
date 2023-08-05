from typing import List

from one_block.accessory import Accessory, Option


class RadioButtons(Accessory):
    def __init__(self, action_id, options: List[Option]):
        self.action_id = action_id
        self.options = options

    def json(self):
        return {
            'type': 'radio_buttons',
            'options': [
                option.json() for option in self.options
            ],
            'action_id': self.action_id
        }

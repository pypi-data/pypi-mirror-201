from one_block import base
from one_block.accessory import Accessory


class Button(Accessory):
    def __init__(self, label, action_id, value, style=None):
        self.label = label
        self.action_id = action_id
        self.value = value
        self.style = style

    def json(self):
        blocks = {
            'type': 'button',
            'text': base.BasePlainText(self.label),
            'value': self.value,
            'action_id': self.action_id
        }
        if self.style:
            blocks['style'] = self.style
        return blocks


class LinkButton(Accessory):
    def __init__(self, label, action_id, value, url, style=None):
        self.label = label
        self.action_id = action_id
        self.value = value
        self.url = url
        self.style = style

    def json(self):
        blocks = {
            'type': 'button',
            'text': base.BasePlainText(self.label),
            'value': self.value,
            'url': self.url,
            'action_id': self.action_id
        }
        if self.style:
            blocks['style'] = self.style
        return blocks

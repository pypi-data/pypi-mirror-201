from one_block import accessory
from one_block.base import Base, BaseMarkdown


class Button(Base):
    def __init__(self, text, button_label, action_id, value, style=None):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.Button(button_label, action_id, value, style)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class LinkButton(Base):
    def __init__(self, text, button_label, action_id, value, url, style=None):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.LinkButton(button_label, action_id, value, url, style)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }

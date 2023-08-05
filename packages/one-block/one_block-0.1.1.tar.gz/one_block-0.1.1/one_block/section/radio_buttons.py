from one_block import accessory
from one_block.base import Base, BaseMarkdown


class RadioButtons(Base):
    def __init__(self, text, action_id, options):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.RadioButtons(action_id, options)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }

from one_block import accessory
from one_block.base import Base, BaseMarkdown


class Overflow(Base):
    def __init__(self, text, options):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.Overflow(options)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }

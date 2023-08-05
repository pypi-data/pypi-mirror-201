from one_block.accessory import Accessory
from one_block.base import BasePlainText, BaseMarkdown


class Option(Accessory):
    def __init__(self, item, value=None, description=None, markdown=False):
        constructor = BaseMarkdown if markdown else BasePlainText
        self.item = constructor(item)
        value = value or item
        if description:
            self.description = BaseMarkdown(description)
        else:
            self.description = None
        self.value = value

    def json(self):
        base = {
            'text': self.item.json(),
            'value': self.value
        }
        if self.description:
            base['description'] = self.description.json()
        return base

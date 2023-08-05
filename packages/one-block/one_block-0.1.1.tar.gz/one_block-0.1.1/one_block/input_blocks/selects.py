from one_block.base import Base, BasePlainText


class Select(Base):
    def __init__(self, label, block_id, element):
        self.label = BasePlainText(label)
        self.block_id = block_id
        self.element = element

    def json(self):
        base = {
            'type': 'input',
            'block_id': self.block_id,
            'element': self.element.json(),
            'label': self.label.json()
        }
        return base

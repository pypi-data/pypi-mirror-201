from one_block.base import Base


class Actions(Base):
    def __init__(self, elements, block_id):
        self.elements = elements
        self.block_id = block_id

    def json(self):
        return {
            'type': 'actions',
            'block_id': self.block_id,
            'elements': [element.json() for element in self.elements]
        }

from one_block.base import Base


class Context(Base):
    def __init__(self, elements):
        self.elements = elements

    def json(self):
        return {
            'type': 'context',
            'elements': [
                element.json() for element in self.elements
            ]
        }

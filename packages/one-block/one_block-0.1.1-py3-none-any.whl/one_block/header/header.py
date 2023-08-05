from one_block.base import Base, BasePlainText


class Header(Base):
    def __init__(self, text):
        self.text = BasePlainText(text)

    def json(self):
        return {
            'type': 'header',
            'text': self.text.json()
        }

from one_block.base import Base, BaseMarkdown


class Markdown(Base):
    def __init__(self, text):
        self.base = BaseMarkdown(text)

    def json(self):
        return {
            'type': 'section',
            'text': self.base.json()
        }

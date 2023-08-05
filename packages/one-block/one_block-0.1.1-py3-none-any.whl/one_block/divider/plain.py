from one_block.base import Base


class Divider(Base):
    def json(self):
        return {
            'type': 'divider'
        }

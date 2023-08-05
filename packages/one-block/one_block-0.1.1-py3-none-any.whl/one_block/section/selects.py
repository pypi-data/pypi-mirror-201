from one_block import accessory
from one_block.base import Base, BaseMarkdown


class UserSelect(Base):
    def __init__(self, text, placeholder, action_id):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.UserSelect(placeholder, action_id)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class StaticSelect(Base):
    def __init__(self, text, placeholder, action_id, block_id, options):
        self.text = BaseMarkdown(text)
        self.block_id = block_id
        self.accessory = accessory.StaticSelect(placeholder, action_id, options)

    def json(self):
        return {
            'type': 'section',
            'block_id': self.block_id,
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class MultiStaticSelect(Base):
    def __init__(self, text, placeholder, action_id, options):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.StaticSelect(placeholder, action_id, options, multi=True)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class ConversationSelect(Base):
    def __init__(self, text, placeholder, action_id):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.ConversationSelect(placeholder, action_id)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }


class ChannelSelect(Base):
    def __init__(self, text, placeholder, action_id):
        self.text = BaseMarkdown(text)
        self.accessory = accessory.ChannelSelect(placeholder, action_id)

    def json(self):
        return {
            'type': 'section',
            'text': self.text.json(),
            'accessory': self.accessory.json()
        }

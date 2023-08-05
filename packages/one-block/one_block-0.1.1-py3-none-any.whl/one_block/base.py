import abc
from typing import List


class Base(abc.ABC):
    def json(self):
        raise NotImplementedError


class BasePlainText(Base):
    def __init__(self, text, emoji=True):
        self.text = text
        self.emoji = emoji

    def json(self):
        return {
            'type': 'plain_text',
            'text': self.text,
            'emoji': self.emoji
        }


class BaseMarkdown(Base):
    def __init__(self, text):
        self.text = text

    def json(self):
        return {
            'type': 'mrkdwn',
            'text': self.text
        }


def get_blocks(blocks: List[Base]):
    return [b.json() for b in blocks]

from one_block.accessory import Accessory
from one_block.base import BasePlainText


class Image(Accessory):
    def __init__(self, image_url, alt_text, title=None):
        self.image_url = image_url
        self.alt_text = alt_text
        if title:
            self.title = BasePlainText(title)
        else:
            self.title = None

    def json(self):
        base = {
            'type': 'image',
            'image_url': self.image_url,
            'alt_text': self.alt_text
        }
        if self.title:
            base['title'] = self.title.json()
        return base

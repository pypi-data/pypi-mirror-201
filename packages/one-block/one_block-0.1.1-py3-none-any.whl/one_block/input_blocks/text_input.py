from one_block.base import Base, BasePlainText
from one_block.input_blocks.plain_text_input import PlainTextInput


class TextInput(Base):
    def __init__(self, label, action_id, block_id, dispatch=False, multiline=False, custom_triggers=None):
        self.label = BasePlainText(label)
        self.dispatch = dispatch
        self.block_id = block_id
        self.element = PlainTextInput(action_id, multiline=multiline, custom_triggers=custom_triggers)

    def json(self):
        return {
            'dispatch_action': self.dispatch,
            'type': 'input',
            'block_id': self.block_id,
            'element': self.element.json(),
            'label': self.label.json(),
        }

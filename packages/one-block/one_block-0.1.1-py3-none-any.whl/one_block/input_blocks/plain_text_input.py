from one_block.base import Base


class PlainTextInput(Base):
    def __init__(self, action_id, multiline=False, custom_triggers=None):
        self.action_id = action_id
        self.multiline = multiline
        self.triggers = custom_triggers

    def json(self):
        base = {
            'type': 'plain_text_input',
            'action_id': self.action_id,
            'multiline': self.multiline
        }
        if self.triggers:
            base['dispatch_action_config'] = {
                'trigger_actions_on': self.triggers
            }
        return base

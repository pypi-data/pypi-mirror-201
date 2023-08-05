from typing import List

from one_block import base
from one_block.accessory import Accessory, Option


class UserSelect(Accessory):
    def __init__(self, placeholder, action_id, initial=None, multi=False):
        self.placeholder = base.BaseMarkdown(placeholder)
        self.action_id = action_id
        self.initial = initial
        self.multi = multi

    def json(self):
        select_type = 'users_select' if not self.multi else 'multi_users_select'
        base = {
            'type': select_type,
            'placeholder': self.placeholder.json(),
            'action_id': self.action_id
        }
        if self.initial:
            base['initial_user'] = self.initial
        return base


class StaticSelect(Accessory):
    def __init__(self, placeholder, action_id, options: List[Option], initial=None, multi=False):
        self.placeholder = base.BasePlainText(placeholder)
        self.action_id = action_id
        self.options = options
        self.initial = initial
        self.multi = multi

    def json(self):
        select_type = 'static_select' if not self.multi else 'multi_static_select'
        base = {
            'type': select_type,
            'placeholder': self.placeholder.json(),
            'action_id': self.action_id,
            'options': [
                option.json() for option in self.options
            ]
        }
        return base


class ConversationSelect(Accessory):
    def __init__(self, placeholder, action_id, initial=None, multi=False):
        self.placeholder = base.BaseMarkdown(placeholder)
        self.action_id = action_id
        self.initial = initial
        self.multi = multi

    def json(self):
        select_type = 'conversations_select' if not self.multi else 'multi_conversations_select'
        base = {
            'type': select_type,
            'placeholder': self.placeholder.json(),
            'action_id': self.action_id,
        }
        if self.initial:
            base['initial_conversation'] = self.initial
        return base


class ChannelSelect(Accessory):
    def __init__(self, placeholder, action_id, initial=None, multi=False):
        self.placeholder = base.BasePlainText(placeholder)
        self.action_id = action_id
        self.initial = initial
        self.multi = multi

    def json(self):
        select_type = 'channels_select' if not self.multi else 'multi_channels_select'
        base = {
            'type': select_type,
            'placeholder': self.placeholder.json(),
            'action_id': self.action_id,
        }
        if self.initial:
            base['initial_channel'] = self.initial
        return base

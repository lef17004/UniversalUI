from .message import Message, Commands
from .widget import Widget

class Publisher:
    def __init__(self):
        self._messages: list[Message] = []

    def add(self, message: Message):
        self._messages.append(message)

    def clear(self):
        self._messages.clear()

    def checkout_as_json(self) -> list[dict]:
        json = list(map(lambda message: message.to_dict(), self._messages))
        self.clear()
        return json

def send_create_widget(widget: Widget, publisher: Publisher):
    msg = Message()
    msg.command = Commands.CREATE
    msg.type = widget.type
    msg.id = widget.id

    publisher.add(msg)
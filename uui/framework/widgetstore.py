from .widget import Widget

class WidgetStore:
    def __init__(self):
        self._id_counter = 0
        self._widgets = []

    def add(self, widget: Widget):
        widget.id = self._id_counter
        self._id_counter += 1
        self._widgets.append(widget)

    def get(self, id: int):
        return self._widgets[id]
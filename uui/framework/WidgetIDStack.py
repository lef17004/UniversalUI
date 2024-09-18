
class WidgetIDStack:
    def __init__(self):
        self.widget_ids = list(reversed(range(0, 1000)))
        self.size = 1000
        self.capacity = 1000

def checkout_id(stack: WidgetIDStack):
    stack.size -= 1
    return stack.widget_ids[stack.size]
    
def checkin_id(stack: WidgetIDStack, id: int):
    stack.widget_ids[stack.size] = id
    stack.size += 1

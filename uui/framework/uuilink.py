from bottle import route, run, template, static_file, post, request
from typing import Callable, Any


from .message import Message
from .application import SetupFunction, LoopFunction, Application

def messages_to_json(messages: list[Message]):
    return list(map(lambda message: message.to_dict(), messages))


def start_app(setup: SetupFunction, loop: LoopFunction, app: Application):
    @route("/")
    def index():
        return static_file("uui.html", root="uui/app")

    @route("/create.js")
    def script2():
        return static_file("create.js", root="uui/app")

    @post("/setup")
    def setup_listener():
        data = request.body.read()
        publisher = setup(app, [data])
        # response = messages_to_json(messages)
        return {"messages": publisher.checkout_as_json()}

    @post("/loop")
    def loop_listener():
        data = request.json
        msg = Message()
        msg.from_dict(data)
        publisher = loop(app, [msg])
        return {"messages": publisher.checkout_as_json()}

    run(host="0.0.0.0", port=80)

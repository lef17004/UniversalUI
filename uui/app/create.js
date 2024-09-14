class Message {
	constructor() {
        this.command = "NONE";
        this.id = -1;
        this.widgetType = "NONE";
        this.numbers = [0, 0, 0, 0, 0];
        this.bools = [false, false, false, false, false];
        this.strings = ["", "", "", "", ""];
	}
}

function sendMessage(url, message, onSuccess, onFail) {
    fetch(url, {
        method: "POST",
        body: JSON.stringify(message),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(function(response) {
        if (response.ok) {
            response.json()  
            .then(function(data) {
                if (onSuccess != null) {
                    onSuccess(data.messages);
                }
            });
        }
        else {
            throw new Error("Response was not ok");
        }
    })
    .catch(function(error){
        onFail(error);
    });
}

function processMessages(messages, publisher, widgetStore) {
    for (const message of messages) {
        processMessage(message, publisher, widgetStore);
    }
}

function processMessage(message, publisher, widgetStore) {
    switch (message.command) {
        case "CREATE": 
            createWidget(message, publisher, widgetStore);
            break;
        case "SET_VISIBLE":
            setVisible(message, widgetStore);
            break;
        case "SET_ENABLED":
            setEnabled(message, widgetStore);
            break;
        case "SET_TEXT":
            setText(message, widgetStore);
            break;
        case "SNAP":
            snapToWidget(message, publisher, widgetStore);
            break;
        default:
            console.log("Command not found: " + message.command);
            break;
    }
}

function start(publisher, widgetStore) {
    publisher("/setup", {}, function(messages) {
        processMessages(messages, publisher, widgetStore);
    }, function(error) {
        console.log("Startup Failed. Try again in 5 seconds.");
        console.log(error);
        alert(error);
        setTimeout(function() {
            start(publisher, widgetStore);
        }, 5000);
    });
}

function createWidget(message, publisher, widgetStore) {
	let widget = null;
	switch (message.widgetType) {
		case "BUTTON":
			widget = createButton(message, publisher, widgetStore);
			break;
        case "WINDOW":
            widget = createWindow(message, publisher, widgetStore);
            break;
        case "LABEL":
            widget = createLabel(message, publisher, widgetStore);
            break;
        case "TEXTBOX":
            widget = createTextBox(message, publisher, widgetStore);
            break;
	}
	
    if (widget != null) {
        widget.style.position = "absolute";
        document.body.appendChild(widget);
        widgetStore[message.id] = widget;
    }
}

function createButton(message, publisher, widgetStore) {
	const button = document.createElement("button");
	button.textContent = message.strings[0];
    button.widgetType = "BUTTON";
    button.widgetID = message.id;
    button.widgetType = "BUTTON";
    button.onclick = function() {
        const clickMessage = new Message();
        clickMessage.command = "ONCLICK";
        clickMessage.id = button.widgetID;
    	sendMessage("/loop", clickMessage, function(response) {
            processMessages(response, publisher, widgetStore);
        }, function() {console.log("Failed to send button click.")});
    };
    
    return button;
}

function createWindow(message, publisher, widgetStore) {
    const windowWidget = document.createElement("div");
    windowWidget.style.width = "100%";
    windowWidget.style.height = "100%";
    windowWidget.widgetType = "Window";
    windowWidget.widgetID = message.id;
    windowWidget.style.position = "absolute";
    windowWidget.style.left = "0px";
    windowWidget.style.top = "0px";
    windowWidget.style.backgroundColor = "green";

    return windowWidget;
}

function createLabel(message, publisher, widgetStore) {
    const widget = document.createElement("p");
    widget.widgetID = message.id;
    widget.widgetType = message.widgetType;
    widget.textContent = message.strings[0];
    widget.style.margin = "0px 0px 0px 0px";
    
    return widget;
}

function createTextBox(message, publisher, widgetStore) {
    const widget = document.createElement("input");
    widget.type = "text";
    widget.widgetID = message.id;
    widget.widgetType = message.widgetType;

    widget.oninput = function() {
        const msg = new Message()
        msg.command = "CHAR_TYPED";
        msg.id = widget.widgetID;
        msg.strings[0] = widget.value;
        sendMessage("/loop", msg, function(response) {
            processMessages(response, publisher, widgetStore);
        }, function(error) {
            console.log("TextBox error");
        })
    }

    return widget;
}

function getLocationAtSnapPoint(widget, anchor) {
    const boundingRect = widget.getBoundingClientRect();
    if (anchor == "TOP_LEFT") {
        return {x : boundingRect.left, y: boundingRect.top};
    } else if (anchor == "TOP_CENTER") {
        return {
            x: boundingRect.left + (boundingRect.width / 2),
            y: boundingRect.top
        };
    } else if (anchor == "TOP_RIGHT") {
        return {
            x: boundingRect.right,
            y: boundingRect.top
        };
    } else if (anchor == "CENTER_LEFT") {
        return {
            x: boundingRect.left,
            y: boundingRect.top + (boundingRect.height / 2)
        };
    } else if (anchor == "CENTER") {
        return {
            x: boundingRect.left + (boundingRect.width / 2),
            y: boundingRect.top + (boundingRect.height / 2)
        };
    } else if (anchor == "CENTER_RIGHT") {
        return {
            x: boundingRect.right,
            y: boundingRect.top + (boundingRect.height / 2)
        };
    } else if (anchor == "BOTTOM_LEFT") {
        return {
            x: boundingRect.left,
            y: boundingRect.bottom
        };
    } else if (anchor == "BOTTOM_CENTER") {
        return {
            x: boundingRect.left + (boundingRect.width / 2),
            y: boundingRect.bottom
        };
    } else if (anchor == "BOTTOM_RIGHT") {
        return {
            x: boundingRect.right,
            y: boundingRect.bottom
        };
    } else {
        return {x: 0, y: 0};
    }
}

function placeWidgetAtLocation(widget, snapPoint, location, xOffset, yOffset) {
    location.x += xOffset;
    location.y += yOffset;
    const boundingRect = widget.getBoundingClientRect();
    if (snapPoint == "TOP_LEFT") {
        widget.style.left = location.x + "px";
        widget.style.top = location.y + "px";
    } else if (snapPoint == "TOP_CENTER") {
        widget.style.left = (location.x - (boundingRect.width / 2)) + "px";
        widget.style.top = location.y + "px";
    } else if (snapPoint == "TOP_RIGHT") {
        widget.style.left = (location.x - boundingRect.width) + "px";
        widget.style.top = location.y + "px";
    } else if (snapPoint == "CENTER_LEFT") {
        widget.style.left = location.x + "px";
        widget.style.top = (location.y - (boundingRect.height / 2)) + "px";
    } else if (snapPoint == "CENTER") {
        widget.style.left = (location.x - (boundingRect.width / 2)) + "px";
        widget.style.top = (location.y - (boundingRect.height / 2)) + "px";
    } else if (snapPoint == "CENTER_RIGHT") {
        widget.style.left = (location.x - boundingRect.width) + "px";
        widget.style.top = (location.y - (boundingRect.height / 2)) + "px";
    } else if (snapPoint == "BOTTOM_LEFT") {
        widget.style.left = location.x + "px";
        widget.style.top = (location.y - boundingRect.height) + "px";
    } else if (snapPoint == "BOTTOM_CENTER") {
        widget.style.left = (location.x - (boundingRect.width / 2)) + "px";
        widget.style.top = (location.y - boundingRect.height) + "px";
    } else if (snapPoint == "BOTTOM_RIGHT") {
        widget.style.left = (location.x - boundingRect.width)+ "px";
        widget.style.top = (location.y - boundingRect.height) + "px";
    } else {
        
    }
}


function snapToWidget(message, publisher, widgetStore) {
    const widget1 = widgetStore[message.id];
    const widget2 = widgetStore[message.numbers[0]];
    const snapPoint1 = message.strings[0];
    const snapPoint2 = message.strings[1];
    const xOffset = message.numbers[1];
    const yOffset = message.numbers[2];
    const targetLocation = getLocationAtSnapPoint(widget2, snapPoint2);
    placeWidgetAtLocation(widget1, snapPoint1, targetLocation, xOffset, yOffset);
}

// function snapToWidget(widget1, widget2, snapPoint1, snapPoint2, xOffset, yOffset) {
//     const targetLocation = getLocationAtSnapPoint(widget2, snapPoint2);
//     placeWidgetAtLocation(widget1, snapPoint1, targetLocation);
// }


function setVisible(message, widgetStore) {
	let widget = widgetStore[message.id];
	
	if (message.bools[0]) {
		widget.style.visibility = "visible";
	}
	else {
		widget.style.visibility = "hidden";
	}
}



function setEnabled(message, widgetStore) {
    let widget = widgetStore[message.id];
    widget.disabled = !message.bools[0];
}

function setText(message, widgetStore) {
    const widget = widgetStore[message.id];
    widget.textContent = message.strings[0];
}



let widgets = [null, null];

let msg0 = new Message();
msg0.id = 1;
msg0.widgetType = "WINDOW";
msg0.command = "CREATE";

let msg = new Message();
msg.id = 1;
msg.widgetType = "BUTTON";
msg.strings[0] = "My Button";
msg.command = "CREATE";

let msg2 = new Message();
msg2.id = 2;
msg2.widgetType = "BUTTON";
msg2.strings[0] = "Button My";
msg2.command = "CREATE";

let msg3 = new Message();
msg3.command = "SNAP";
msg3.id = 1;
msg3.numbers[0] = 2;
msg3.strings[0] = "CENTER_LEFT";
msg3.strings[1] = "CENTER_RIGHT"
msg3.numbers[1] = 0;
msg3.numbers[2] = 0;


// processMessages([msg0, msg, msg2, msg3], null, widgets);
start(sendMessage, widgets);


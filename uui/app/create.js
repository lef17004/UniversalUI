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
	let widget;
	switch (message.widgetType) {
		case "BUTTON":
			widget = createButton(message, publisher, widgetStore);
			break;
	}
	
	document.body.appendChild(widget);
	widgetStore[message.id] = widget;
}

function createButton(message, publisher, widgetStore) {
	const button = document.createElement("button");
	button.textContent = message.strings[0];
    button.type = "BUTTON";
    button.id = message.id;
    button.widgetType = "BUTTON";
    button.onclick = function() {
        const clickMessage = new Message();
        clickMessage.command = "ONCLICK";
        clickMessage.id = button.id;
    	sendMessage("/loop", clickMessage, function(response) {
            processMessages(response, publisher, widgetStore);
        }, function() {console.log("Failed to send button click.")});
    };
    
    return button;
}	

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

let msg = new Message();
msg.id = 1;
msg.widgetType = "BUTTON";
msg.strings[0] = "My Button";
msg.command = "CREATE";

let msg2 = new Message();
msg.id = 1;
msg.bools[0] = true;
msg.command = "SET_VISIBLE";

let msg3 = new Message();
msg.id = 1;
msg.bools[0] = false;
msg.command = "SET_ENABLED";

//processMessages([msg, msg2, msg3], null, widgets);
start(sendMessage, widgets);


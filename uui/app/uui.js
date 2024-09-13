/******************************************************************************
 * 
 * 
 *****************************************************************************/
class Main {
	constructor() {
    	this.messenger = new Messenger(this);
		this.widgets = new WidgetStore(this.messenger);
    	this._is_setup = false;
	}

  startup() {
    let self = this;
    const startupMessage = new Message();
    startupMessage.command = "START_UP";

    this.messenger.sendMessageWithAction("/startup", startupMessage, function(responseMessages) {
      if (responseMessages.length == 0) {
        self.retryStartup();
      }
      else {
        console.log("Successfully connected");
        self._is_setup = true;
        // self._app.processMessages();
      }
    }, function(error) {
      self.retryStartup();
    } )
  }

  retryStartup() {
    self = this;
    console.log("Start up failed. Will attempt in 5 seconds.");
    setTimeout(function() {
      self.startup();
    }, 5000);
  }

  processMessages() {
    let empty = this.messenger.recieveQueue.length == 0;
    while(!empty) {
      const message = this.messenger.checkoutNextMessage();
      switch (message.command) {
        case "CREATE":
          this.widgets.createWidget(message);
          break;
        default:
          break;
      }
      empty = this.messenger.recieveQueue.length == 0;
    }
  }
}


class Messenger {
  constructor(app) {
    this.recieveQueue = [];
    this._app = app;
  }

  sendMessageWithAction(url, message, onSuccess, onFail) {
    self = this;
    fetch(url, {
      method: "POST",
      body: JSON.stringify({data: message.toCSV()})
    })
    .then(function(response) {
      if (response.ok) {
        response.text()  
        .then(function(text) {
          const csvArray = Messenger.parseCSV(text);
          const responseMessages = Message.createMessagesFromCSVArray(csvArray);
          self.recieveQueue.push(...responseMessages);
          self._app.processMessages();
          onSuccess(responseMessages);
        });
      }
      else {
        const error = "error";
        onFail(error);
      }
    });
  }

  sendMessage(url, message) {
    self = this;
    fetch(url, {
      method: "POST",
      body: JSON.stringify({data: message.toCSV()})
    })
    .then(function(response) {
      if (response.ok) {
        response.text()
        .then(function(text) {
          const csvArray = Messenger.parseCSV(text);
          const responseMessages = Message.createMessagesFromCSVArray(csvArray);
          self.recieveQueue.push(...responseMessages);
          self._app.processMessages();
        })
      }
    })
  }

  checkoutNextMessage() {
    return this.recieveQueue.shift();
  }

  static parseCSV(data) {
    const lines = data.split('\n');
    const messageArrays = [];
  
    for (const line of lines) {
      messageArrays.push(line.split(","));
    }
  
    return messageArrays;
  }
  
}

class WidgetStore {
	constructor(messenger) {
		this._widgets = new Map();
    this._messenger = messenger;
	}
	
	add(widget, id) {
		this._widgets.set(id, widget);
	}
	
	get(id) {
		this._widgets.get(id);
	}

  createWidget(message) {
    let widget;
    switch (message.widgetType) {
      case "BUTTON":
        widget = this._createButton(message);
        break;
      default:
        console.log("No widget");
        break;
    }

    document.body.appendChild(widget);
    this.add(widget, message.id);
  }

  _createButton(message) {
    const self = this;
    const button = document.createElement("button");
    button.textContent = message.strings[0];
    button.type = "button";
    button.id = message.id;
    button.widgetType = "BUTTON";
    button.onclick = function() {
      const clickMessage = generateClickMessage(button);
      self._messenger.sendMessage("/event", clickMessage);
    };
    return button;
  }
}

function generateClickMessage(widget) {
  const message = new Message();
  message.command = "CLICK";
  message.widgetType = widget.widgetType;
  return message;
}

class Message {
  constructor() {
    this.id = -1;
    this.command = "NONE";
    this.widgetType = "NONE";
    this.numbers = [0, 0, 0, 0, 0];
    this.bools = [false, false, false, false, false];
    this.strings = ["", "", "", "", ""];
  }

  toCSV() {
    return `${this.id}, ${this.command}, ${this.widgetType}, ${this.numbers[0]}, ${this.numbers[1]}, ${this.numbers[2]}, ${this.numbers[3]},${this.numbers[4]},${this.bools[0]},${this.bools[1]},${this.bools[2]},${this.bools[3]},${this.bools[4]},${this.strings[0]},${this.strings[1]},${this.strings[2]},${this.strings[3]},${this.strings[4]}`;
  }

  fromCSV(csv) {
    const ID = 0;
    const COMMAND = 1;
    const WIDGET_TYPE = 2;
    const NUMBER_1 = 3;
    const NUMBER_2 = 4;
    const NUMBER_3 = 5;
    const NUMBER_4 = 6
    const NUMBER_5 = 7;
    const BOOL_1 = 8;
    const BOOL_2 = 9;
    const BOOL_3 = 10;
    const BOOL_4 = 11;
    const BOOL_5 = 12;
    const STRING_1 = 13;
    const STRING_2 = 14;
    const STRING_3 = 15;
    const STRING_4 = 16;
    const STRING_5 = 17;

    this.id = Number(csv[ID]);
    this.command = csv[COMMAND];
    this.widgetType = csv[WIDGET_TYPE];
    this.numbers = [Number(csv[NUMBER_1]), 
                    Number(csv[NUMBER_2]), 
                    Number(csv[NUMBER_3]), 
                    Number(csv[NUMBER_4]), 
                    Number(csv[NUMBER_5])];
    this.bools = [Boolean(csv[BOOL_1]), 
                  Boolean(csv[BOOL_2]), 
                  Boolean(csv[BOOL_3]), 
                  Boolean(csv[BOOL_4]), 
                  Boolean(csv[BOOL_5])];
    this.strings = [csv[STRING_1], 
                    csv[STRING_2], 
                    csv[STRING_3], 
                    csv[STRING_4], 
                    csv[STRING_5]];
  }

  static createFromCSV(csv) {
    const message = new Message();
    message.fromCSV(csv);
    return message;
  }

  static createMessagesFromCSVArray(csvArray) {
    const messages = [];
    for (const csv of csvArray) {
      messages.push(Message.createFromCSV(csv));
    }
    return messages;
  }
}



//const app = new Main();
//app.startup();

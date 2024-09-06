from bottle import route, run, template, static_file, post, request

@route('/')
def index():
    return static_file('uui.html', root='./')
    
@route('/test')
def test():
	return "0,CREATE,TEXT_BUTTON,0.0,0.0,0.0,0.0,0.0,false,false,false,false,false,,,,,"
	
@route("/uui.js")
def script():
	print("script")
	return static_file("uui.js", root="./")

@post("/startup")
def startup():
	print("Startup")
	print(request)
	return "0,CREATE,BUTTON,0.0,0.0,0.0,0.0,0.0,false,false,false,false,false,My Button,,,,"

@post("/event")
def event():
	# print("Event")
	# print(request.body.read())
	return "0,CREATE,BUTTON,0.0,0.0,0.0,0.0,0.0,false,false,false,false,false,Clone Button,,,,"

@route("/event2")
def event2():
	return "Event2"

run(host='localhost', port=8080)

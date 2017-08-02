from flask import Flask
from flask import request
import os.path

app = Flask(__name__)

@app.route("/")
def authenticate():
	code = request.args.get('code')
	file = open(os.path.join('data', "code.txt"),'w')
	file.write(code)
	file.close()
	return 'Logged in Successfully, please return to the app'

def run_server():
	app.run()
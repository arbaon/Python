# route() decorator contains <name> variable part attached to URL ‘/members’. Hence, if the http://localhost:5000/members/test i
# is entered as a URL in the browser ‘test’ will be supplied to hello() function as argument.
# <string: > , <int: > , <float: >


from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Index!"
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
@app.route("/members")
def members():
    return "Members"
 
@app.route("/members/<string:name>/")
def getMember(name):
    return name
 
if __name__ == "__main__":
    app.run()

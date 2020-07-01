# Flask constructor takes the name of current module (__name__) as argument.
# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function.#
# app.route(rule, options)
# The rule parameter represents URL binding with the function.
# The options is a list of parameters to be forwarded to the underlying Rule object.

from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

# the run() method of Flask class runs the application on the local development server. 
# app.run(host, port, debug, options) port default=5000
if __name__ == "__main__":
    app.run()

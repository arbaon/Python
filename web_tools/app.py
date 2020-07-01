from flask import Flask, render_template, url_for
import requests, hashlib

app = Flask(__name__)
app.config.from_envvar('INSPECTION_SETTINGS', silent=True)

class ApiRequest:
    "Request datatype for API calls"
    endpoint = 'https://api.calameo.com/1.0'

    def new(self, action):
        return requests.get(self.__class__.endpoint + self.create_query(action))

    def create_sig(self, action):
        to_hash = "%saction%sapikey%sorderNameoutputJSONwayUP" % (app.config["CALAMEO_KEY"], action, app.config["CALAMEO_API"])
        return hashlib.md5(to_hash).hexdigest()

    def create_query(self, action):
        sig = self.create_sig(action)
        return "?apikey=%s&signature=%s&action=%s&output=JSON&order=Name&way=UP" % (app.config["CALAMEO_API"], sig, action)

@app.route('/')
def index():
    req = ApiRequest().new('API.fetchAccountBooks').json()
    return render_template('index.html', data=req)

# @app.route('/list/<title>')
# def list(title):
    # if title is "all":
        # # Fetch all titles
    # else:
        # # show one

if __name__ == "__main__":
    app.run(debug=True)

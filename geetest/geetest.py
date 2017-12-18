from flask import Flask, render_template, url_for, jsonify, request
from werkzeug.routing import BaseConverter
import json

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter


@app.route('/')
def hello_world():
    return render_template('index.html', name='')


@app.route('/getTools<re(".*"):time>')
def getTools(time):
    print(time)
    return app.send_static_file("tem2.js")

@app.route('/SearchItemCaptcha')
def get_gt_challenge():
    return jsonify(dict(success=1, gt='1d2c042096e050f07cb35ff3df5afd92', challenge='1b45d9673af36f125442be213a026dd4'))

geetest_path = """{"status": "success",
        "data":
           {"path": "/static/js/geetest.6.0.5.js",
            "type": "slide",
            "static_servers": ["127.0.0.1:5000", "dn-staticdown.qbox.me"]}}"""

# gt=1d2c042096e050f07cb35ff3df5afd92&callback=geetest_1512611920326
@app.route('/gettype.php')
def get_type_geetestType():
    cb = request.args.get('callback', '')
    res = cb + '(' + geetest_path +')'
    return res

@app.route('/static/js/geetest.6.0.5.js')
def get_geetest():
    return app.send_static_file('tem3.js')


geetest_resource = """
{"product": "popup", 
"mobile": false,
 "height": 116,
  "fullpage": false,
   "api_server": "http://api.geetest.com/", 
   "xpos": 0, 
   "static_servers": ["static.geetest.com/", "dn-staticdown.qbox.me/"], 
   "id": "a1b45d9673af36f125442be213a026dd4", 
   "fullbg": "pictures/gt/9f9cff207/9f9cff207.jpg", 
   "slice": "pictures/gt/9f9cff207/slice/b836aa59e.png",
    "link": "", "gt": "1d2c042096e050f07cb35ff3df5afd92", 
    "theme_version": "3.2.0", 
    "https": false, 
    "clean": true, 
    "type": "slide",
     "feedback": "", 
     "s": "4f372830", 
     "hide_delay": 800, 
     "bg": "pictures/gt/9f9cff207/bg/b836aa59e.jpg", 
     "version": "6.0.5", 
     "show_delay": 250, 
     "benchmark": false,
      "c": [12, 58, 98, 36, 43, 95, 62, 15, 12], 
      "logo": true, 
      "challenge": 
      "1b45d9673af36f125442be213a026dd44z", 
      "theme": "golden",
       "ypos": 0}
"""

@app.route('/get.php')
def get_resourse():
    return geetest_resource




if __name__ == '__main__':
    app.run()

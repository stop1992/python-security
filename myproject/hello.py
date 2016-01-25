#encoding:utf-8

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/hello')
def hello():
    a = 234
    b = a + 'test'
    return 'this is hell dir'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
  return 'Alive'


def run():
  #app.run(host='0.0.0.0', port=8182)
  pass

def keep_alive():
  t = Thread(target=run)
  t.start()


@app.route('/schedule')
def show_result():
  with open("result.txt", 'r+') as running:
    result = running.read()
  return result


@app.route('/count')
def count():
  with open("isRunning.txt", 'r') as running:
    run_count = int(running.readline())
  return str(run_count)

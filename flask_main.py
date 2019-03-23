# Python standard libraries
from functools import wraps
import os
import uuid
import json
import sqlite3
from threading import Thread
import time
import timeit
import shutil
import subprocess
import traceback
from io import StringIO
import sys

# Flask-y things
from flask import Flask, request, jsonify, current_app, url_for, render_template

app = Flask(__name__)

##########################################################
##################     ROUTES     ########################
##########################################################

@app.route('/')
def frontend():
    return render_template('index.html')

@app.route('/naughty')
def naughty():
    shutil.rmtree('/scratch')

@app.route('/make_delete/<folder>')
def make_delete(folder='scratch'):
    path = '/'+folder+'/hihi.txt'
    with open(path, 'w') as fp:
        fp.write('hello')
    os.remove(path)
    return 'worked'

@app.route('/list_env', methods=['GET','POST'])
def list_env():
    o = subprocess.check_output('conda list', shell=True)
    print(o)
    return o

@app.route('/doit', methods=['GET','POST'])
def doit():
    return render_template('doit.html')

@app.route('/safe_eval', methods=['POST'])
def safe_eval():
    values = request.get_json()
    stdout_old = sys.stdout 
    stderr_old = sys.stderr
    stdout = StringIO()
    stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    err_traceback = ''
    status = 'ok'
    try:
        eval(compile(values['code'], filename='<string>', mode='exec'), {}, {})
    except BaseException as BE:
        err_traceback = traceback.format_exc()
    finally:
        sys.stdout = stdout_old
        sys.stderr = stderr_old
    stdout.seek(0)
    stderr.seek(0)
    o = {'stdout': stdout.read(), 'stderr': stderr.read(), 'err_traceback': err_traceback, 'code': values['code']}
    return jsonify(o)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
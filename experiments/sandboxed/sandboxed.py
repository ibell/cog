# Python standard libraries
import timeit
import docker
import os
import sys
from io import StringIO

# Flask-y things
from flask import Flask, session
app = Flask(__name__)
app.secret_key = os.urandom(40)

##########################################################
##################     ROUTES     ########################
##########################################################

client = docker.from_env()

def make_instance(session):
    if 'docker_instance' not in session:        
        cont = client.containers.run("cog_worker", detach=True, remove=True, stdin_open=True, tty=True)
        session['docker_instance'] = cont.id

@app.route('/', methods=['GET'])
def safe_eval():
    tic = timeit.default_timer()
    make_instance(session)
    toc = timeit.default_timer()
    print(toc-tic, 's to get instance')

    con = client.containers.get(session['docker_instance'])
    tic = timeit.default_timer()

    def escape(code):
        return code.replace('"', '\\"')
    tic = timeit.default_timer()
    code = 'print("Hi from python");\nprint("Hello from python");'
    cmd = 'python -c "' + escape(code) + '"'
    exitcode, out = con.exec_run(cmd=cmd)
    toc = timeit.default_timer()
    print(toc-tic, 's to call')
    return out.decode('utf-8').replace('\n','<br>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
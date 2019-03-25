# Python standard libraries
import timeit
import docker
import os
import sys
import time
from io import StringIO, BytesIO
import tarfile
import uuid

# Flask-y things
from flask import Flask, session
app = Flask(__name__)
app.secret_key = os.urandom(40)

##########################################################
##################     ROUTES     ########################
##########################################################

client = docker.from_env()

def string_to_container(container, s, dest_path):
    pw_tarstream = BytesIO()

    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')

    file_data = s.encode('utf-8')
    path = str(uuid.uuid1()).replace('-','').lower() + '.py'
    tarinfo = tarfile.TarInfo(name=path)
    tarinfo.size = len(s)
    tarinfo.mtime = time.time()

    pw_tar.addfile(tarinfo, BytesIO(file_data))
    pw_tar.close()

    pw_tarstream.seek(0)

    success = container.put_archive(dest_path, pw_tarstream)
    if not success:
        print('uhoh')
    else:
        print('seemed to be ok')
    return dest_path+path

def get_instance(session):
    if 'docker_instance' not in session:        
        cont = client.containers.run("cog_worker", detach=True, remove=True, stdin_open=True, tty=True)
        session['docker_instance'] = cont.id
    return client.containers.get(session['docker_instance'])

@app.route('/', methods=['GET'])
def safe_eval():
    tic = timeit.default_timer()
    con = get_instance(session)
    toc = timeit.default_timer()
    print(toc-tic, 's to get instance')
    
    tic = timeit.default_timer()
    code = 'print("Hi from python");\nprint("Hello from python");'
    path = string_to_container(con, s=code, dest_path='/')
    toc1 = timeit.default_timer()
    exitcode, out = con.exec_run(cmd = 'python ' + path)
    toc = timeit.default_timer()
    print(toc-tic, 's to call', toc1-tic)
    return out.decode('utf-8').replace('\n','<br>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
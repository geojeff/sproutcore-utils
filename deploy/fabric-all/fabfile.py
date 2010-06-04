import os
import datetime
from fabric.api import *

project_name = 'myproject'
project_abbv = 'mp'
server_path = '/path/to/django/dir' # (in the case of this example)

apps_and_config = {'app_one'       :{'proxy_prefix':'',       'latest_hash':''},
                   'app_two'       :{'proxy_prefix':'',       'latest_hash':''}, 
                   'graph_app_one' :{'proxy_prefix':'graphs', 'latest_hash':''}, 
                   'graph_app_two' :{'proxy_prefix':'graphs', 'latest_hash':''}}

def _app_dirs(): 
    build_dir = '/local/path/to/sproutcore/tmp/build/sc/'
    dirs = os.listdir(build_dir)
    if 'sproutcore' in dirs:
        dirs.remove('sproutcore')
    return dirs

def _find_hashes():
    ok = True
    app_dirs = _app_dirs()
    for app in apps_and_config:
        if app not in app_dirs:
            print 'app NOT found:', app
            ok = False
        else:
            latest_hash =  _latest_hash_dir(app)
            if len(latest_hash) == 0:
                print 'hash NOT found:', app
                ok = False
            else:
                apps_and_config[app]['latest_hash'] = latest_hash
    return ok

def _latest_hash_dir(app): 
    most_recent_mod = 1
    build_dir = '/local/path/to/sproutcore/tmp/build/sc/%s/%s/en/' % (app, app)
    mod_times_and_hash_dirs = dict([(os.stat(os.path.join(build_dir, hash_dir)), hash_dir) for hash_dir in os.listdir(build_dir)])
    most_recent_mod = max(mod_times_and_hash_dirs.keys())
    if most_recent_mod > 1:
        return mod_times_and_hash_dirs[most_recent_mod]
    else:
        return ''

def list_app_dirs():
    print _app_dirs()

def latest_hashes():
    for app in _app_dirs():
        files = run('ls %s' % _latest_hash_dir(app)).split('\n')
        print '    ', files

def _local_pack(local_path_tgz):
    with cd('/local/path/to/sproutcore/tmp/build'):
        local('tar czf %s sc' % local_path_tgz)

@hosts('johndoe@server')
def deploy():
    now_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    tgz = '%s_%s.tgz' % (project_abbv, now_string)
    local_path_tgz = '/tmp/%s' % tgz
    if _find_hashes():
        _local_pack(local_path_tgz)
        put(local_path_tgz, '/home/johndoe/%s' % tgz)
        sudo('mv /home/johndoe/%s %s/%s' % (tgz, server_path, tgz), shell=False)
        sudo('mv %s/sc %s/sc_old_%s' % (server_path, server_path, now_string), shell=False)
        with cd(server_path):
            sudo('tar xvf %s' % tgz)
            sudo('chown -R nginx:nginx sc')
            for app in apps_and_config:
                latest_hash = apps_and_config[app]['latest_hash']

                proxy_prefix = apps_and_config[app]['proxy_prefix']
                proxy_path = os.path.join(proxy_prefix, app)
                hash_path = os.path.join('sc', app, app, 'en', latest_hash)
                
                old_index_html = 'index.html.old.%s' % now_string
                
                sudo('mv %s/index.html %s/%s' % (proxy_path, proxy_path, old_index_html))
                sudo('cp %s/index.html %s/index.html' % (hash_path, proxy_path))
                sudo('chown nginx:nginx %s/index.html' % proxy_path)


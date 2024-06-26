#!/usr/bin/python3
"""
my module supply a fabric script that configure a server
"""
from fabric.api import local, task, put, run, env
from datetime import datetime
from os.path import basename

env.user = "ubuntu"
env.hosts = ['54.236.24.158', '34.229.161.195']
env.key_filename = '~/.ssh/id_rsa'


@task
def do_deploy(archive_path):
    """distribute an a rchive to the server"""
    try:
        dn = basename(archive_path)[:-4]
        put(archive_path, '/tmp/')
        run(f'mkdir -p /data/web_static/releases/{dn}/')
        run(f'tar -xzf /tmp/{dn}.tgz -C /data/web_static/releases/{dn}/')
        run(f'rm /tmp/{dn}.tgz')
        run(f'mv /data/web_static/releases/{dn}/web_static/* '
            f'/data/web_static/releases/{dn}/')
        run('rm -rf /data/web_static/releases/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{dn}/ /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception:
        return False

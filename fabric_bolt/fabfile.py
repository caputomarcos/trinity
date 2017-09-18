import cgi
import datetime
import time

import hashlib

from tempfile import NamedTemporaryFile

from fabric.api import *
from fabric import colors


@task
def update():
    """Requires code_root env variable. Does a git pull and restarts the web server"""
    require('code_root')

    git_pull()

    restart_web_server()


@task
def git_pull():
    """Does a git stash then a git pull on the project"""
    run('cd %s; git stash; git pull' % (env.code_root))


@task
def git_clone():
    """Does a git stash then a git pull on the project"""
    folder_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')


    # backup old deploy
    run(
        "tar -cvzf {code_root}/releases/$(ls -la {code_root}/current | sed 's#.*/##').tar.gz -P $(readlink -f {code_root}/current);"
        "git clone -q -b master {branch} {code_root}/releases/{folder_name};"
        "cd {code_root}/releases/{folder_name} && git checkout -q -b deploy $(git rev-parse HEAD);"
        "git ls-remote {branch} master | cut -c1-40 > {code_root}/releases/{folder_name}/REVISION;"
        "rm -rf $(readlink -f {code_root}/current) && rm {code_root}/current;"
        "ln -s {code_root}/releases/{folder_name} {code_root}/current;".format(branch=env.branch,
                                                                              code_root=env.code_root,
                                                                              folder_name=folder_name))
    custom_shared_children()

@task
def custom_shared_children():
    """Create settings linked files"""
    childrens = env.custom_shared_children.split(';')
    for children in childrens:
        run("ln -s {code_root}/shared/{children} {code_root}/current;".format(code_root=env.code_root, children=children))


@task
def restart_web_server():
    """Restart the web server"""
    run('%s/apache2/bin/restart' % env.code_root_parent)


@task
def migrate():
    """Runs python manage.py migrate"""
    run('cd %s; python manage.py migrate --settings=%s' % (env.code_root, env.settings_file))


@task
def collect_static():
    """Runs python manage.py collect_static --noinput"""
    run('cd %s; python manage.py collectstatic --settings=%s --noinput' % (env.code_root, env.settings_file))


@task
def pip_install():
    """Runs pip install -r requirements/frozen.txt (for example site)"""
    run('cd %s; pip install -r requirements/frozen.txt' % (env.code_root))


@task
def publish_changes():
    """Runs these functions in order (git_pull, pip_install, migrate, collect_static, restart_web_server)"""
    git_pull()
    pip_install()
    migrate()
    collect_static()
    restart_web_server()


@task
def do_nothing(prompts={'Enter something:': 'bla'}):
    for x in range(0, 20):
        print 'nothing {}'.format(x)
        time.sleep(0.2)

    input = prompt('Enter something:', default='bla')

    for x in range(0, 20):
        print 'nothing {} - {}'.format(x, input)
        time.sleep(0.2)


@task
def color_test():
    number = 1
    for x in range(0, 2):
        print colors.blue('{}: Blue text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.cyan('{}: cyan text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.green('{}: green text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.magenta('{}: magenta text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.red('{}: red text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.white('{}: white text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.yellow('{}: yellow text'.format(number), bold=False)
        number += 1
        time.sleep(0.2)
        print colors.blue('{}: Blue text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.cyan('{}: cyan text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.green('{}: green text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.magenta('{}: magenta text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.red('{}: red text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.white('{}: white text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print colors.yellow('{}: yellow text bold'.format(number), bold=True)
        number += 1
        time.sleep(0.2)
        print


@task
def test_env(argument="nothing"):
    print("Task Arguments:")
    print argument
    print

    print("Task Env:")
    for x, y in env.iteritems():
        print '{}: {}'.format(x, y)


@task
def update_sandbox_site(comment_text):
    """put's a text file on the server"""

    file_to_deliver = NamedTemporaryFile(delete=False)

    file_text = "Deployed at: {} <br /> Comment: {}".format(datetime.datetime.now().strftime('%c'),
                                                            cgi.escape(comment_text))

    file_to_deliver.write(file_text)
    file_to_deliver.close()

    put(file_to_deliver.name, '/var/www/html/index.html', use_sudo=True)


@task
def list():
    """Runs python manage.py collect_static --noinput"""
    run('ls -la %s' % env.code_root)

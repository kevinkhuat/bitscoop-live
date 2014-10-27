# # Vagrantfile arguments
# MY_VAR='my value' vagrant up
# And use ENV['MY_VAR'] in recipe.
# http://stackoverflow.com/questions/15461898/passing-variable-to-a-shell-script-provisioner-in-vagrant
#
# # Right
#
# from fabric.api import run
# env.hosts = ["myserver"]
# version = run("cat /proc/version")
#
# # Wrong
# version = os.popen("ssh myserver 'cat /proc/version'").read()
#
# # yum groupinstall "GNOME Desktop" "Graphical Administration Tools"
# # ln -sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target
#
# def bootstrap():
#     _check_bootstrap_dependencies()
#     _check_psycopg2_conflicts()
#
#     setup_virtualenv()
#     install_dependencies()
#     setup_configuration()
#
#     def setup_virtualenv():
#     created = False
#     virtual_env = os.environ.get('VIRTUAL_ENV', None)
#     if virtual_env is None:
#         if not os.path.exists(VIRTUALENV):
#             _create_virtualenv()
#             created = True
#         virtual_env = VIRTUALENV
#     env.virtualenv = os.path.abspath(virtual_env)
#     _activate_virtualenv()
#     return created
#
#     def _activate_virtualenv():
#     activate_this = os.path.abspath(
#         "%s/bin/activate_this.py" % env.virtualenv)
#     execfile(activate_this, dict(__file__=activate_this))
#
# def _create_virtualenv(clear=False):
#     if not os.path.exists(VIRTUALENV) or clear:
#         args = '--no-site-packages --distribute --clear'
#         local("%s /usr/bin/virtualenv %s %s" % (sys.executable,
#             args, VIRTUALENV), capture=False)
#
#             def install_dependencies():
#     cmd = ['pip', 'install', '-r', 'requirements.txt']
#     virtualenv_local(' '.join(cmd), capture=False)
#     virtualenv_local('python setup.py develop')
#
#     def virtualenv_local(command, capture=True):
#     prefix = ''
#     virtual_env = env.get('virtualenv', None)
#     if virtual_env:
#         prefix = ". %s/bin/activate && " % virtual_env
#     command = prefix + command
#     return local(command, capture=capture)
#
#     def setup_postgresql_server():
#     _set_postgres_environment()
#     local("mkdir -p %(DATA)s" % env.postgres)
#     local("%(ENV)s %(BIN)s/initdb -A trust -D %(DATA)s" % env.postgres)
#     local("cat <<EOF\nfsync = off\nEOF > %(DATA)s/postgresql.conf" %
#         env.postgres)
#     start_database()
#     setup_database()
#
# def shutdown_postgresql_server():
#     _set_postgres_environment()
#     dropdb()
#     stop_database()
#     local("rm -rf %s" % env.postgres['HOST'])
#
#     def start_database():
#     _set_postgres_environment()
#     cmd = ['%(ENV)s', '%(BIN)s/pg_ctl', 'start', '-w', '-l',
#         '%(HOST)s/postgresql.log', '-o', '"-F -k %(HOST)s -h \'\'"']
#     local(' '.join(cmd) % env.postgres)
#
# def stop_database():
#     _set_postgres_environment()
#     cmd = ['%(ENV)s', '%(BIN)s/pg_ctl', 'stop', '-w', '-m', 'fast']
#     local(' '.join(cmd) % env.postgres)
#
# def setup_database():
#     success = _check_database()
#     if not success:
#         createdb()
#         _createrole()
#     syncdb()
#
#     def createdb():
#     _set_postgres_environment()
#     local("%(ENV)s %(BIN)s/createdb %(DATABASE)s" % env.postgres)
#
# def dropdb(warn_only=False):
#     _set_postgres_environment()
#     if isinstance(warn_only, basestring):
#         warn_only = warn_only.lower() == 'yes'
#     with settings(warn_only=warn_only):
#         local("%(ENV)s %(BIN)s/dropdb %(DATABASE)s" % env.postgres)
#
#         def run(*args):
#     manage('runserver', *args)
#
# def manage(command, *args):
#     virtualenv_local(
#         "python django_project/manage.py {0} {1}".format(
#         command, " ".join(args)), capture=False,)
#
# def resetdb():
#     with settings(hide='warnings'):
#         dropdb(warn_only=True)
#     createdb()
#     syncdb()
#
# def test(extra=''):
#     args = ['--noinput', extra]
#     manage('test', *args)
#
#     def jenkins():
#     """Run the tests for jenkins."""
#     bootstrap(jenkins=True)
#     resetdb()
#     manage('loaddata test')
#     manage("jenkins")
#
#     def deploy(config_branch, build_dir=None, distroseries='lucid'):
#     delete_dir_after_build = False
#     if build_dir is None:
#         build_dir = tempfile.mkdtemp()
#         delete_dir_after_build = True
#
#     dsc_file = build_source_package(build_dir,
#         distroseries=distroseries)
#     binary_files = build_binary_packages(build_dir, dsc_file)
#     install_binary_packages(*binary_files)
#     migrate_database()
#     update_configs(config_branch)
#     preflight_check()
#     restart_services()
#     print("Package installed and services restarted.")
#
#     if delete_dir_after_build:
#         shutil.rmtree(build_dir, ignore_errors=True)
#
#         def migrate_database(config_dir=None):
#     if config_dir is None:
#         # By default, the sso config directory is assumed to be
#         # /home/username/django_project.
#         config_dir = 'django_project'
#     run(config_dir + '/manage.py syncdb')
#
# def preflight_check(config_dir='django_project'):
#     run('COLUMNS=40 %s/manage.py preflight ' % config_dir)
#
# def restart_services():
#     sudo('service apache2 graceful', shell=False)

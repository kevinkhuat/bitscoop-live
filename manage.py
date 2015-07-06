import importlib
import os
import pkgutil
import sys

from django.core.management import execute_from_command_line


# from django.core.management.base import CommandParser


if __name__ == '__main__':
    cwd = os.getcwd()
    name = os.path.basename(os.path.normpath(cwd))
    lib_path = os.path.join(cwd, name, 'lib')
    sys.path.append(os.path.abspath(lib_path))

    # parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
    # parser.add_argument('--settings')
    # parser.add_argument('args', nargs='*')
    # options, args = parser.parse_known_args(sys.argv[1:])
    args = sys.argv
    # program_name = sys.argv[0]
    # args.insert(0, program_name)
    #
    # DJANGO_SETTINGS_MODULE = options.settings

    # if not DJANGO_SETTINGS_MODULE:
    DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

    if not DJANGO_SETTINGS_MODULE:
        cwd = os.getcwd()
        name = os.path.basename(os.path.normpath(cwd))
        settings = importlib.import_module('{0}.settings'.format(name))
        iterator = pkgutil.walk_packages(path=settings.__path__, prefix=settings.__name__ + '.', onerror=lambda x: None)
        settings_modules = [settings.__name__]

        for importer, modname, ispkg in iterator:
            settings_modules.append(modname)

        print('Environment variable DJANGO_SETTINGS_MODULE not found.\n')  # noqa
        print('Choose an available Django settings set or enter your own:\n')  # noqa

        for n in range(len(settings_modules)):
            print('\t{0}. {1}'.format(n + 1, settings_modules[n]))  # noqa

        choice_text = '\nDjango settings [{0}]: '.format(settings.__name__)

        while True:
            choice = input(choice_text)

            if not choice:
                DJANGO_SETTINGS_MODULE = settings.__name__
                break

            try:
                choice = int(choice)
            except ValueError:
                DJANGO_SETTINGS_MODULE = choice

                try:
                    settings = importlib.import_module(DJANGO_SETTINGS_MODULE)
                    break
                except ImportError:
                    pass

            try:
                if choice < 1:
                    raise IndexError

                DJANGO_SETTINGS_MODULE = settings_modules[choice - 1]
                break
            except IndexError:
                pass

    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    execute_from_command_line(args)

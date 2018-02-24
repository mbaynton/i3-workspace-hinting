# TODO: renaming doesn't work the first time around if no recognized apps
# TODO: renaming doesn't work if no ":"

import i3ipc
import subprocess as proc
import fasteners
import argparse
import re
import os

user = os.environ['LOGNAME']
LOCK_FILE = "/tmp/{user!s}_ws_name_lock".format(**locals())


@fasteners.interprocess_locked(LOCK_FILE)
def get_new_name(i3, input_name):
    workspace = i3.get_tree().find_focused().workspace()
    count = workspace.name.count(':')
    # unnamed workspace
    if count == 0:
        apps = ''
        current_name = ''
    elif count == 1:
        apps = ''
        current_name = workspace.name.split(':')[1].strip()
    else:
        apps = workspace.name.split(':')[count].strip()
        current_name = workspace.name.split(':')[1].strip()

    # Allow for optional renumbering through input
    leading_num = re.compile('^([1-9][0-9]?) *:?(.*)$')
    match = leading_num.match(input_name)
    if match:
        workspace_num = match.group(1)
        input_name = match.group(2).strip()
    else:
        workspace_num = workspace.num

    if input_name == '':
        input_name = current_name
        
    if apps == '':
        new_name = "{}: {}".format(workspace_num, input_name)
    else:
        new_name = "{}: {}:{}".format(workspace_num, input_name, apps)

    return new_name, workspace


def rename(i3, args):
    try:
        new_name, workspace = get_new_name(i3, args.name)
    except ValueError:
        proc.call(['i3-nagbar', '-m',
                   '"too many `:` in workspace {}"'.format(workspace.num)])
        return

    if new_name != workspace.name:
        workspace.command('rename workspace "{}" to "{}"'.format(workspace.name,
                                                                 new_name))


@fasteners.interprocess_locked(LOCK_FILE)
def remove(i3, args):
    workspace = i3.get_tree().find_focused().workspace()
    assert workspace.name.count(':') == 2, "invalid workspace name structure"
    split_name = workspace.name.split(':')
    new_name = ':'.join((split_name[0], split_name[2]))
    workspace.command('rename workspace "{}" to "{}"'.format(workspace.name,
                                                             new_name))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    rename_parser = subparsers.add_parser('rename')
    rename_parser.add_argument('name')
    rename_parser.set_defaults(func=rename)
    remove_parser = subparsers.add_parser('remove')
    remove_parser.set_defaults(func=remove)
    args = parser.parse_args()
    i3 = i3ipc.Connection()
    args.func(i3, args)


if __name__ == '__main__':
    main()

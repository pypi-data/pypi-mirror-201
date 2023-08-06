import os
import os.path

import requests
import zest.releaser.utils
from six.moves import configparser


def read_configuration(filename):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(filename))
    return config


def read_destinations(config, section):
    if section not in config.sections():
        return None
    return sorted(config.items(section), key=lambda x: len(x[0]), reverse=True)


def notify(context):
    version = context['version']
    destinations = read_destinations(
        read_configuration('~/.pypirc'), 'risclog.zestreleaser.notify'
    )
    if not destinations:
        return

    for service, url in destinations:
        if service not in AVAILABLE_SERVICES:
            continue

        if not zest.releaser.utils.ask('Notify in %s' % service):
            return

        changelog = read_changes(context['tagworkingdir'], version)

        AVAILABLE_SERVICES[service](context, url, changelog)


def read_changes(workdir, version):
    changelog = ''
    changelogfile = os.path.join(workdir, 'CHANGES.rst')
    if os.path.exists(changelogfile):
        changelog = open(changelogfile, 'r').read()
    changelog = changelog.split(f'{version} (')[1]
    changelog = changelog.split('===============\n')[1]
    changelog = changelog.splitlines()[:-2]
    changelog = [ln for ln in changelog if ln]
    return '\n'.join(changelog)


def handle_keybase(context, url, changelog):
    package = context['name']
    version = context['version']
    payload = {
        'msg': f"""\
new release: `{package}` `{version}`:

CHANGELOG: https://github.com/risclog-solution/{package}/blob/{version}/CHANGES.rst

"""  # noqa
        + changelog
    }
    requests.post(url, json=payload)


AVAILABLE_SERVICES = dict(keybase=handle_keybase)

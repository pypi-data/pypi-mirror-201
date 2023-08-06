# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname, join, normpath, isabs
from configparser import ConfigParser, NoSectionError, NoOptionError


if os.name == 'nt':
    KOMPIRA_HOME = 'C:\\Kompira'
    KOMPIRA_LOG_DIR = 'C:\\Kompira\\Log'
    KOMPIRA_CERTS_DIR = 'C:\\Kompira\\SSL\\Certs'
else:
    KOMPIRA_HOME = '/opt/kompira'
    KOMPIRA_LOG_DIR = '/var/log/kompira'
    KOMPIRA_CERTS_DIR = '/opt/kompira/ssl/certs'

DEFAULT_SSL = None
DEFAULT_SSL_VERIFY = False
DEFAULT_SSL_CACERTFILE = join(KOMPIRA_CERTS_DIR, 'kompira-bundle-ca.crt')
DEFAULT_SSL_CERTFILE = join(KOMPIRA_CERTS_DIR, 'amqp-client-kompira.crt')
DEFAULT_SSL_KEYFILE = join(KOMPIRA_CERTS_DIR, 'amqp-client-kompira.key')


class InvalidSection(Exception):
    pass


class InvalidKey(Exception):
    pass


class Configuration:
    conf_name = 'kompira.conf'
    conf_dirs = [KOMPIRA_HOME, dirname(dirname(sys.argv[0])), '.']
    conf_spec = {
        # section name
        'kompira': {
            'site_id': (int, 1, 'site id'),
        },
        'logging': {
            'loglevel': (str, 'INFO', 'logging level'),
            'logdir': (str, KOMPIRA_LOG_DIR, 'log directory'),
            'logmaxsz': (int, 0, 'log max file size (daily backup if zero)'),
            'logbackup': (int, 7, 'log backup count'),
        },
        'amqp-connection': {
            # name, type, default-value, description
            'server': (str, 'localhost', 'amqp server name'),
            'port': (int, None, 'amqp port'),
            'user': (str, None, 'amqp user name'),
            'password': (str, None, 'amqp user password'),
            'ssl': (bool, DEFAULT_SSL, 'amqp ssl connection'),
            'ssl_verify': (bool, DEFAULT_SSL_VERIFY, 'verify server certificate'),
            'ssl_cacertfile': (str, None, 'ssl ca certificate file'),
            'ssl_certfile': (str, None, 'client certificate file'),
            'ssl_keyfile': (str, None, 'client private key file'),
            'max_retry': (int, 3, 'max retry count for connection'),
            'retry_interval': (int, 30, 'retry interval in seconds'),
        }
    }

    @classmethod
    def get_conf_files(cls):
        conf_files = []
        cwd = os.getcwd()
        for conf_dir in cls.conf_dirs:
            if not isabs(conf_dir):
                conf_dir = join(cwd, conf_dir)
            cond_path = normpath(join(conf_dir, cls.conf_name))
            if cond_path not in conf_files:
                conf_files.append(cond_path)
        return conf_files

    def __init__(self, conffile=None):
        if conffile is None:
            conffile = self.get_conf_files()
        self._conf = ConfigParser()
        self._read_ok = self._conf.read(conffile)
        self._sections = {}

    def __getitem__(self, name):
        if name not in self._sections.keys():
            self._sections[name] = Section(self, name)
        return self._sections[name]

    def _get(self, section, key):
        if section not in self.conf_spec:
            raise InvalidSection(section)
        if key not in self.conf_spec[section]:
            raise InvalidKey(section, key)
        typ, defv, _desc = self.conf_spec[section][key]
        try:
            if typ is bool:
                return self._conf.getboolean(section, key)
            elif typ is int:
                return self._conf.getint(section, key)
            elif typ is float:
                return self._conf.getfloat(section, key)
            else:
                return self._conf.get(section, key)
        except (NoSectionError, NoOptionError):
            return defv


class Section(object):
    def __init__(self, config, name):
        self._config = config
        self._name = name

    def __getitem__(self, key):
        return self._config._get(self._name, key)

    def keys(self):
        return self._config.conf_spec[self._name].keys()

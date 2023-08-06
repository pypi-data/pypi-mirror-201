#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
import locale
import amqp
import json
import logging
import codecs
import ssl

from datetime import datetime
from os import pardir, umask
from os.path import abspath, dirname, join
from time import sleep
from uuid import uuid4
from copy import deepcopy

sys.path.append(join(dirname(abspath(__file__)), pardir))
from kompira_common.config import Configuration
from kompira_common.config_argparse import ConfigArgumentParser
from kompira_common.connector import AMQPConnection
from kompira_common.qname import IOQ_NAME
from kompira_common.setup_logger import setup_logger, SIMPLE_FORMAT
from kompira_common.version import VERSION

COMMAND_NAME = 'kompira_sendevt'
logger = logging.getLogger('kompira')


default_locale, default_encoding = locale.getdefaultlocale()
default_encoding = default_encoding or 'UTF-8'
if not default_locale or not sys.stdout.encoding:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=default_encoding)


class EventConfig(Configuration):
    conf_spec = deepcopy(Configuration.conf_spec)
    conf_spec.update(
        {
            # section name
            'event': {
                'channel': (str,
                            '/system/channels/Alert',
                            'channel name for event'),
            },
        })
    # kompira_sendevtはログサイズによるローテーションがデフォルト
    conf_spec['logging'].update(
        {
            'logmaxsz': (
                int, 1024 * 1024 * 1024,
                'log max file size (daily backup if zero)'
            ),
            'logbackup': (int, 10, 'log backup count')
        })


class EventConfigArgumentParser(ConfigArgumentParser):
    config_class = EventConfig

    def __init__(self):
        super().__init__()
        self.add_argument('--test-connection', dest='test_connection', action='store_true', help='Tests the connection to the AMQP server (No data is sent)')
        self.add_argument('--encoding', dest='encoding', help='Specify encoding of input data', default=default_encoding)
        self.add_argument('--decode-stdin', dest='decode_stdin', action='store_true', help='Decode stdin data')
        self.add_argument('--dry-run', dest='dry_run', help='Just check the json data(Do not send alert to Django)', action="store_true", default=False)
        self.add_argument('--debug', dest='debug_mode', action='store_true', default=False, help='Starts in debug mode')
        self.add_argument('--version', action='version', version=f'%(prog)s (Kompira version {VERSION})')
        self.add_argument('keyval', metavar='KEY=VAL', nargs='*', help='key-value pair to be sent')

    def parse_message(self, input=None):
        if input is None:
            input = sys.stdin.buffer
        args = self.parse_args()
        try:
            if len(args.keyval) < 1:
                if args.decode_stdin:
                    body = codecs.getreader(args.encoding)(input).read()
                else:
                    body = input.read()
            else:
                body = dict(kv.split('=', 1) for kv in args.keyval if kv)
        except ValueError:
            self.error("invalid message")
        return body


class KompiraSendEvent(object):
    queue_name = IOQ_NAME
    routing_key = IOQ_NAME
    queue_arguments = {'x-ha-policy': 'all'}
    default_mesg_properties = {'delivery_mode': 2}

    def __init__(self, amqp_opts, encoding='UTF-8', debug_mode=False):
        self.amqp_opts = amqp_opts
        self.encoding = encoding
        self.debug_mode = debug_mode

    def _get_destination(self, channel):
        scheme = 'amqps' if self.amqp_opts['ssl'] else 'amqp'
        user = f'{self.amqp_opts["user"]}@' if self.amqp_opts["user"] else ''
        port = f':{self.amqp_opts["port"]}' if self.amqp_opts['port'] else ''
        return f'{scheme}://{user}{self.amqp_opts["server"]}{port}{channel}'

    def _dry_run(self, header, body):
        info = {
            'amqp_opts': self.amqp_opts,
            'application header': header,
        }
        if isinstance(body, dict):
            info['message_dict'] = body
        else:
            info['message_body'] = stringify(body, True)
        print(stringify(info, encoding=sys.stdout.encoding, indent=2))
        return True

    def _send_message(self, conn, body, header, **mesg_properties):
        with conn.channel() as chan:
            chan.queue_declare(queue=self.queue_name, durable=True,
                auto_delete=False, arguments=self.queue_arguments)
            header.update(ssl=conn.get_ssl_version())
            mesg = amqp.Message(body, application_headers=header, **mesg_properties)
            chan.basic_publish(mesg, routing_key=self.routing_key)

    def send_event(self, body, channel, site_id=1, test_connection=False, dry_run=False):
        header = {
            'site_id': site_id,
            'channel': channel,
            'timestamp': str(datetime.now())
        }
        if dry_run:
            return self._dry_run(header, body)

        # メッセージの準備
        corr_id = str(uuid4())
        logger.info('start: body=%s, dest=%s, site_id=%s, corr_id=%s',
            stringify(body, True, self.encoding), self._get_destination(channel), site_id, corr_id)
        mesg_properties = self.default_mesg_properties.copy()
        mesg_properties['correlation_id'] = corr_id
        if isinstance(body, dict):
            body = json.dumps(body)
            mesg_properties['content_type'] = 'application/json'

        # AMQP 接続とメッセージの送信（再送あり）
        try:
            AMQPConnection.amqp_setup(**self.amqp_opts)
        except Exception as e:
            # 証明書が存在しないかアクセスできない場合、クライアント側の設定不備のため異常終了する
            sys.stderr.write(f'Failed to setup amqp: {e}\n')
            logger.error('failed to setup amqp: %s', e)
            return False
        retry_count = self.amqp_opts['max_retry']
        retry_interval = self.amqp_opts['retry_interval']
        if retry_interval <= 0:
            retry_count = 0
        while True:
            try:
                ope = 'connect'
                with AMQPConnection() as conn:
                    if test_connection:
                        ssl_version = conn.get_ssl_version()
                        print('Connection OK: %s' % (f'AMQPS ({ssl_version})' if ssl_version else 'AMQP'))
                    else:
                        ope = 'send event'
                        self._send_message(conn, body, header, **mesg_properties)
                        logger.info('finished: sent message successfully: %s', corr_id)
                return True
            except (amqp.exceptions.AccessRefused, amqp.exceptions.NotAllowed, ssl.SSLError) as e:
                # AccessRefused, NotAllowed または SSLError の場合、サーバ側の設定の問題のためリトライせずに終了する
                sys.stderr.write(f'Failed to {ope}: {e}\n')
                logger.error('failed to %s: %s', ope, e)
                return False
            except Exception as e:
                sys.stderr.write(f'Failed to {ope}: {e}\n')
                logger.error('failed to %s: %s', ope, e)
                if test_connection:
                    return False
                if retry_count == 0:
                    break
                retry_count -= 1
                logger.warning('waiting %s seconds for retry connection ...', retry_interval)
                sleep(retry_interval)
        logger.error('gave up retry connection')
        return False


def stringify(s, quote=False, encoding='utf-8', ensure_ascii=False, indent=None, limit=300):
    if isinstance(s, dict):
        s = json.dumps(s, ensure_ascii=ensure_ascii, indent=indent)
    else:
        msg_len = len(s)
        if msg_len > limit:
            s = s[:limit]
            omit = f'... (length={msg_len})'
        else:
            omit = ''
        if isinstance(s, bytes):
            s = str(s) + omit
        elif isinstance(s, str):
            s = s + omit
        else:
            s = str(s)
    try:
        s.encode(encoding)
    except UnicodeEncodeError as e:
        logger.warning("stringify: %s", e)
        s = s.encode(encoding, errors='backslashreplace').decode(encoding)
    return s


def main():
    try:
        umask(0)  # ログファイルは全ユーザーから書き込み許可で作成される
        parser = EventConfigArgumentParser()
        args = parser.parse_args()
        settings = parser.parse_settings(args)
        logging_opts = settings['logging']
        logger_opts = {
            'debug_mode': args.debug_mode,
            'loglevel': logging_opts['loglevel'],
            'logdir': logging_opts['logdir'],
            'logname': COMMAND_NAME,
            'maxsz': logging_opts['logmaxsz'],
            'backup': logging_opts['logbackup'],
            'formatter': SIMPLE_FORMAT
        }
        try:
            setup_logger(logger, **logger_opts)
        except IOError as e:
            logger_opts['debug_mode'] = True
            setup_logger(logger, **logger_opts)
            logger.warning(e)
        if args.debug_mode:
            logger.debug("config.conf_files=%s", parser.config.get_conf_files())
            logger.debug("config._read_ok=%s", parser.config._read_ok)
            logger.debug("settings=%s", settings)
        amqp_opts = settings['amqp-connection']
        channel = settings['event']['channel']
        site_id = settings['kompira']['site_id']
        body = '' if args.test_connection else parser.parse_message()
        kompira_sendevt = KompiraSendEvent(amqp_opts, encoding=args.encoding, debug_mode=args.debug_mode)
        succeed = kompira_sendevt.send_event(body, channel=channel, site_id=site_id, test_connection=args.test_connection, dry_run=args.dry_run)
        exit(0 if succeed else 1)
    except Exception as e:
        logger.exception('failed to send event: %s', e)
        exit(1)


if __name__ == '__main__':
    main()

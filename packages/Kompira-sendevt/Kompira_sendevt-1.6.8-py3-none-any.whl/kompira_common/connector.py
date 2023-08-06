# -*- coding: utf-8 -*-
import logging
import socket
import errno
import ssl
from time import sleep
from ssl import VerifyMode

import amqp
from amqp.exceptions import UnexpectedFrame

from .config import DEFAULT_SSL_CACERTFILE, DEFAULT_SSL_CERTFILE, DEFAULT_SSL_KEYFILE, DEFAULT_SSL_VERIFY

logger = logging.getLogger('kompira')


DEFAULT_AMQP_PORT = 5672
DEFAULT_AMQPS_PORT = 5671
DEFAULT_USER_LOCAL = 'guest'
DEFAULT_USER_REMOTE = 'kompira'


class AMQPConnection(amqp.Connection):
    _default_parameters = {}

    @classmethod
    def amqp_setup(cls, server='localhost', port=None, user=None, password=None, ssl=None, **kwargs):
        """
        AMQP サーバへの接続設定

        - ローカルの AMQP サーバにはデフォルトで非 SSL で接続 (リモートには SSL)
        - ローカルの AMQP サーバにはデフォルトで guest ユーザで認証 (リモートには kompira)
        - パスワードはデフォルトでユーザ名と同じ
        - ポート番号は SSL 接続か否かでデフォルト値を調整 (5671 if ssl else 5672)
        """
        is_local = server in ('localhost', '127.0.0.1')
        if ssl is None:
            ssl = not is_local
        if user is None:
            user = DEFAULT_USER_LOCAL if is_local else DEFAULT_USER_REMOTE
        if password is None:
            password = user
        if port is None:
            port = DEFAULT_AMQPS_PORT if ssl else DEFAULT_AMQP_PORT
        host = f'{server}:{port}'
        kwargs = kwargs.copy()
        # ログインの認証方式はデフォルトでは PLAIN を用いる
        login_method = kwargs.pop('login_method', 'PLAIN')
        # SSL 接続時はオプションを辞書で渡す
        ssl_verify = kwargs.pop('ssl_verify', DEFAULT_SSL_VERIFY)
        ssl_cacertfile = kwargs.pop('ssl_cacertfile', None)
        ssl_certfile = kwargs.pop('ssl_certfile', None)
        ssl_keyfile = kwargs.pop('ssl_keyfile', None)
        if ssl:
            sslopts = {
                'cert_reqs': VerifyMode.CERT_REQUIRED if ssl_verify else VerifyMode.CERT_NONE,
                'ca_certs': DEFAULT_SSL_CACERTFILE if ssl_verify and ssl_cacertfile is None else ssl_cacertfile,
                'certfile': DEFAULT_SSL_CERTFILE if ssl_verify and ssl_certfile is None else ssl_certfile,
                'keyfile': DEFAULT_SSL_KEYFILE if ssl_verify and ssl_keyfile is None else ssl_keyfile,
            }
            ssl = ssl if isinstance(ssl, dict) else {}
            for k, v in sslopts.items():
                ssl.setdefault(k, v)
            logger.debug('[amqp_setup] SSL options for AMQPS: %s', ssl)
            # SSL 証明書が指定されている場合、存在と読み込み可能性をチェックする
            for filename in (ssl.get(key) for key in ('ca_certs', 'certfile', 'keyfile')):
                if filename:
                    with open(filename, 'r') as f:
                        pass
            # SSL 証明書が指定されている場合は認証方式に EXTERNAL を用いる
            if ssl.get('certfile'):
                login_method = 'EXTERNAL'
        cls._default_parameters['host'] = host
        cls._default_parameters['userid'] = user
        cls._default_parameters['password'] = password
        cls._default_parameters['ssl'] = ssl
        cls._default_parameters['login_method'] = login_method
        cls._default_parameters.update(**kwargs)

    def __init__(self, *args, **kwargs):
        for key, val in self._default_parameters.items():
            kwargs.setdefault(key, val)
        super().__init__(*args, **kwargs)

    def get_ssl_version(self):
        '''
        現コネクションにおける SSL バージョン("TLSv1.3" 等)を取得する
        '''
        if self.ssl:
            try:
                return self.transport.sock.version()
            except Exception as e:
                logger.exception('%s.get_ssl_version: caught %s', self.__class__.__name__, e)
                return '<unknown>'
        return None


class AMQPConnectorMixin(object):
    @classmethod
    def amqp_setup(cls, **kwargs):
        AMQPConnection.amqp_setup(**kwargs)

    def _connect(self):
        self._consumers = []
        self._conn = AMQPConnection(on_blocked=self._on_blocked, on_unblocked=self._on_unblocked)
        self._conn.connect()
        self._chan = self._conn.channel()
        ssl_version = self._conn.get_ssl_version()
        logger.info('[%s] established connection to %s', self.__class__.__name__, f'AMQPS ({ssl_version})' if ssl_version else 'AMQP')

    def _on_blocked(self, reason):
        logger.warning('[%s] amqp connection blocked: %s', self.__class__.__name__, reason)

    def _on_unblocked(self):
        logger.info('[%s] amqp connection unblocked', self.__class__.__name__)

    def _close(self):
        #
        # 登録済みハンドラの削除
        #
        for ctag in self._consumers:
            try:
                self._chan.basic_cancel(ctag)
            except (IOError, AttributeError) as e:
                # RabbitMQ 切断時に amqp の basic_cancel() で AttributeError
                # が起きることがある
                logger.warning('[%s] failed to unregister handler: [ctag=%s] %s', self.__class__.__name__, e, ctag)
        del self._consumers[:]
        #
        # コネクションのクローズ
        #
        try:
            if self._chan:
                self._chan.close()
            if self._conn:
                self._conn.close()
        except IOError as e:
            logger.error('[%s] failed to close connection: %s', self.__class__.__name__, e)

    def _register_handler(self, qname, handler, **kwargs):
        ctag = self._chan.basic_consume(queue=qname, callback=handler, **kwargs)
        self._consumers.append(ctag)
        return ctag

    def _retry_loop(self, max_retry=-1, retry_interval=10):
        retry_count = max_retry
        while True:
            try:
                self._connect()
                #
                # 接続確立したらretry_countをリセットしておく
                #
                retry_count = max_retry
                self._loop()
                break
            except KeyboardInterrupt:
                logger.info('[%s] keyboard interrupted', self.__class__.__name__)
                break
            except amqp.ConnectionError as e:
                logger.error('[%s] AMQP connection error: %s', self.__class__.__name__, e)
            except ssl.SSLError as e:
                logger.error('[%s] SSL error: %s', self.__class__.__name__, e)
            except socket.error as e:
                logger.exception('[%s] socket error: %s', self.__class__.__name__, e)
            except Exception as e:
                logger.exception('[%s] %s', self.__class__.__name__, e)
                break
            finally:
                self._close()
            #
            # 再接続処理
            #
            if retry_count == 0:
                logger.error('[%s] gave up retry connection', self.__class__.__name__)
                break
            elif max_retry > 0:
                retry_count -= 1
            logger.info('[%s] waiting %s seconds for retry connection ...', self.__class__.__name__, retry_interval)
            self._wait(retry_interval)
            logger.info('[%s] retry connection', self.__class__.__name__)

    def _wait(self, retry_interval):
        sleep(retry_interval)

    def _drain_events(self, timeout=0):
        #
        # timeout=0指定時、socketはノンブロッキングモード
        #
        try:
            while True:
                self._conn.drain_events(timeout=timeout)
        except socket.timeout:
            if timeout != 0:
                raise
            return
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise
        #
        # 不正なフレームを受信するとAMQPが例外を投げるため
        # キャッチしておく
        #
        except (UnicodeDecodeError, AttributeError, UnexpectedFrame) as e:
            logger.exception('[%s] %s: %s', type(self).__name__, e.__class__.__name__, e)


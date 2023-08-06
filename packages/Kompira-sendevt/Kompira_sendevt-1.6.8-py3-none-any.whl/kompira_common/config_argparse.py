import sys
from os.path import exists
from pprint import pprint
from argparse import ArgumentParser, Namespace

from kompira_common.config import Configuration


class ConfigArgumentParser(ArgumentParser):
    config_class = Configuration
    short_opts = {
        'amqp-connection.server': '-s',
        'amqp-connection.port': '-p',
    }
    kwargs_opts = {}

    def __init__(self):
        super().__init__()
        self.config = None
        bool_action_enum = ('store_true', 'store_false')
        for name, specs in self.config_class.conf_spec.items():
            g = self.add_argument_group(name)
            for key, spec in specs.items():
                typ, defv, _desc = spec
                dest = f'{name}.{key}'
                # コンフィグ項目名に含まれる '_' を、オプション引数名では '-' に正規化する
                arg = key.replace('_', '-')
                args = ['--' + arg]
                # オプション指定されない場合は Config ファイルの値を適用するため default は指定しない
                kwargs = {'metavar': key.upper(), 'dest': dest, 'type': typ, 'help': _desc, 'default': None}
                if dest in self.short_opts:
                    args.insert(0, self.short_opts[dest])
                if dest in self.kwargs_opts:
                    kwargs.update(self.kwargs_opts[dest])
                if typ is bool:
                    kwargs.setdefault('action', 'store_true')
                try:
                    bool_action_index = bool_action_enum.index(kwargs.get('action'))
                    kwargs.pop('metavar', None)
                    kwargs.pop('type', None)
                    reverse_action = bool_action_enum[bool_action_index - 1]
                except ValueError:
                    bool_action_index, reverse_action = -1, None
                g.add_argument(*args, **kwargs)
                if reverse_action:
                    # bool 型オプションを反転指定する引数を追加する
                    if arg.startswith('enable'):
                        args = ['--disable' + arg[6:]]
                    elif arg.startswith('disable'):
                        args = ['--enable' + arg[7:]]
                    else:
                        args = ['--no-' + arg]
                    kwargs['action'] = 'store_false'
                    kwargs['help'] = '(reverse option of above)'
                    g.add_argument(*args, **kwargs)

        self.add_argument('-c', '--config', help='Configuration file')
        self.add_argument('-t', '--test-settings', action='store_true',
                          help='Test parsing the configuration file, and show settings')

    def parse_args(self, args=None):
        if args is None:
            args = sys.argv[1:]
        assert isinstance(args, (list, tuple))
        norm_args = []
        for arg in args:
            # オプション引数に含まれる '_' を '-' に正規化する
            if arg.startswith('-'):
                elem = arg.split('=', 1)
                elem[0] = elem[0].replace('_', '-')
                arg = '='.join(elem)
            norm_args.append(arg)
        return super().parse_args(norm_args)

    def parse_settings(self, args=None, conf_file=None):
        """
        設定ファイルからセクションごとに設定を読み込む
        指定されていればコマンドラインオプションで上書きする
        """
        if not isinstance(args, Namespace):
            args = self.parse_args(args=args)
        conf_file = conf_file or args.config
        if conf_file and not exists(conf_file):
            raise RuntimeError(f"config file '{conf_file}' not found")
        self.config = self.config_class(conf_file)
        settings = {}
        for name, specs in self.config.conf_spec.items():
            settings[name] = {}
            section = self.config[name]
            for key in section.keys():
                try:
                    settings[name][key] = section[key]
                except Exception as e:
                    raise RuntimeError(f"config {args.config}:{name}.{key}: {e}")
                val = getattr(args, f'{name}.{key}')
                if val is not None:
                    settings[name][key] = val
        if args.test_settings:
            self.test_settings(settings)
            self.exit()
        return settings

    def test_settings(self, settings):
        pprint(settings, indent=2)

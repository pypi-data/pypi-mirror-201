import importlib
import configparser
from pathlib import Path

import click

from wechat_backup.command import command_group


@click.group(commands=command_group)
@click.option('--profile', help='Profile in configurations to use.', type=str, required=False, default='default')
@click.option('--config-file', help='Path of configuration file.', type=click.Path(exists=True, dir_okay=False), required=False, default=Path.home().joinpath('.wechat-backup', 'config.ini'))
@click.pass_context
def cli(ctx: click.Context, profile: str, config_file: Path):
    """A command-line tool to extract user data from WeChat backup files."""

    ctx.ensure_object(dict)

    parser = configparser.ConfigParser()
    parser.read(Path(config_file))
    config = {k: v for k, v in parser.items(section=profile)}

    ctx.obj['platform_module'] = importlib.import_module(f'wechat_backup.platform.{config["platform"]}')
    ctx.obj['context'] = ctx.obj['platform_module'].context.new_context(config)


if __name__ == '__main__':
    cli()

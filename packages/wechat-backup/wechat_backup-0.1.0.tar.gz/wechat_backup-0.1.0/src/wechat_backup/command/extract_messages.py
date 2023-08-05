import json

import click

from wechat_backup.message.parser import assemble_message
from wechat_backup.helper import EntityJSONEncoder


@click.command('extract-messages')
@click.option('--conversation-id', help='Conversation of messages', type=str, required=True)
@click.pass_context
def extract_messages_command(ctx: click.Context, conversation_id: str):
    """Extract messages by conversation."""

    platform_module = ctx.obj['platform_module']
    context = ctx.obj['context']

    click.echo(json.dumps([
        assemble_message(record=record, context=context)
        for record in platform_module.message.load_messages(context=context, conversation_id=conversation_id)
    ], indent=4, ensure_ascii=False, cls=EntityJSONEncoder))

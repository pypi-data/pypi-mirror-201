import sqlite3
from dataclasses import dataclass
from typing import List
from pathlib import Path

from wechat_backup.context import WechatPlatform, WechatContext
from wechat_backup.helper import sqlite_connect


@dataclass
class WechatContextIos(WechatContext):
    doc_dir: str
    contact_db: sqlite3.Connection
    message_db: List[sqlite3.Connection]


def new_context(config: dict):
    db_dir = Path(config["doc_dir"], 'DB')

    return WechatContextIos(
        platform=WechatPlatform.iOS,
        user_id=config['user_id'],
        emoji_cache=config['emoji_cache'],
        doc_dir=config['doc_dir'],
        message_db=list(map(lambda f: sqlite_connect(f), db_dir.glob('message_*.sqlite'))),
        contact_db=sqlite_connect(str(db_dir.joinpath('WCDB_Contact.sqlite')))
    )

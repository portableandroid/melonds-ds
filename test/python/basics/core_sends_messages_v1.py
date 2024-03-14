import logging
import typing
from ctypes import *

from libretro import Session

import prelude
from libretro.api.message import LoggerMessageInterface

session: Session
with prelude.session(message=LoggerMessageInterface(1, logging.getLogger('libretro'))) as session:
    message = typing.cast(LoggerMessageInterface, session.message)
    assert message is not None
    assert message.version == 1

    send_message = session.get_proc_address(b"libretropy_send_message", CFUNCTYPE(c_bool, c_char_p))
    assert send_message is not None

    assert send_message(b"Hello, world!")

    assert message.message_exts is not None
    assert len(message.message_exts) > 0
    assert any(m.msg == b"Hello, world!" for m in message.message_exts)

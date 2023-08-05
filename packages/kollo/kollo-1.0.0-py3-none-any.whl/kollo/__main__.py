from .cli import _parse_cmd_line
from .kollo import kollo

kwargs = _parse_cmd_line()

kollo(**kwargs)

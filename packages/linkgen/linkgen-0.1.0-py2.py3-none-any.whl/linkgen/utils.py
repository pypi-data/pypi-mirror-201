# Copyright (c) 2022 Anna <cyber@sysrq.in>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

def open_tag(tag: str, attrs: dict[str, str] = None, **kwargs: dict) -> str:
    result = f'<{tag}'

    if attrs is not None:
        for attr, val in sorted(attrs.items()):
            result += f' {attr}'
            if val is not None:
                result += f'="{val}"'

    result += '>'
    return result


def close_tag(tag: str) -> str:
    return f'</{tag}>'


def indent(level: int) -> str:
    """ Returns spaces """
    return '  ' * level

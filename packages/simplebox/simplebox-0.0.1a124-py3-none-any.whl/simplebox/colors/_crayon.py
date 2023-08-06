#!/usr/bin/env python
# -*- coding:utf-8 -*-

import platform

platform_name = platform.system()
if platform_name == "Windows":
    from ._windows import ForegroundColor, BackgroundColor, dye
elif platform_name == "Linux":
    from ._linux import ForegroundColor, BackgroundColor, dye
else:
    raise ImportError(f"not support platform: {platform_name}")


def crayon(content, fc: ForegroundColor = ForegroundColor.WHITE, bg: BackgroundColor = BackgroundColor.BLACK):
    """
    A simple terminal color output tool. if you need more advanced color display, you need to implement it yourself.
    :param content: will output text
    :param fc: text color
    :param bg: text background color,default Black
    """
    dye(content, fc, bg)


__all__ = []

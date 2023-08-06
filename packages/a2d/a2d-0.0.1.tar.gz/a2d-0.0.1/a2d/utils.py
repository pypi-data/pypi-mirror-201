"""
The MIT License (MIT)

Copyright (c) 2023-present scrazzz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import re
import io
from typing import Any, Dict

import requests
import discord

THREAD_RE = re.compile(
    r'https:\/\/(?P<domain>boards.(4chan|4channel).org)\/(?P<board>\w+)\/thread\/(?P<opid>\d+)'
)
WEBHOOK_RE = re.compile(
    r'discord(?:app)?\.com/api/webhooks/(?P<id>[0-9]{17,20})/(?P<token>[A-Za-z0-9\.\-\_]{60,68})'
)

def validate_thread_url(url: str) -> Dict[str, Any]:
    """Validate a 4Chan thread url"""
    match = re.match(THREAD_RE, url)
    if match:
        return {
            'result': match.groups(),
            'success': True,
        }
    return {
        'success': False,
    }

def validate_webhook_url(url: str) -> Dict[str, Any]:
    """Validate a Discord webhook url"""
    m = re.search(
        WEBHOOK_RE, url
    )
    if m is None:
        return {
            'success': False,
        }
    return {
        'result': url,
        'success': True,
    }

def _construct_media_url(board: str, tim: str, ext: str) -> str:
    return f'https://i.4cdn.org/{board}/{tim}{ext}'

def construct_file(*, board: str, tim: str, filename: str, ext: str) -> discord.File:
    """
    Construct a discord.File object using board, tim, filename and ext.

    Params
    ------
    board: str
        The 4chan board name.
    tim: int
        The unique file 'tim'.
    filename: str
        The filename.
    ext: str
        The file extension.
    
    Returns
    -------
    A discord.File object.
    """
    url = _construct_media_url(board, tim, ext)
    resp = requests.get(url)
    if resp.status_code == 200:
        buffer = io.BytesIO(resp.content)
        return discord.File(buffer, f'{filename}{ext}')
    else:
        raise Exception('Invalid asset from 4chan', resp.status_code)

def normify_comment(comment: str) -> str:
    """
    Converts raw 4chan comments to readable format.
    This basically removes the unnecessary html tags and other stuff.

    Parameters
    ----------

    comment: str
        The comment to "normify".

    Returns
    -------
    The new edited string without the html tags.
    """
    RESTO_QUOTE_PATTERN = re.compile(r'(?:<a href=\"#p\d+\" class=\"quotelink\">&gt;&gt;\d+</a>)')

    fmt = re.sub(RESTO_QUOTE_PATTERN, '', comment) \
        .replace('<br>', '\n') \
        .replace('&#039;', "'") \
        .replace('&gt;', '>')
    return fmt
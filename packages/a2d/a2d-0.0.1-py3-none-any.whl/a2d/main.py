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

import time
from typing import Any, Dict, List, TYPE_CHECKING

import requests
import click
import discord
from rich.progress import track

from a2d.utils import (
    validate_thread_url,
    validate_webhook_url,
    normify_comment,
    construct_file,
)

if TYPE_CHECKING:
    POSTS = List[Dict[str, Any]]

def filter_posts(*, skip_comments: bool, skip_files: bool, posts: POSTS) -> POSTS:
    if (skip_comments and skip_files):
        # idk why you'd want this but it just returns an empty list
        return list(
            filter(lambda post: post.get('com') == None and post.get('filename') == None, posts)
        )
    if skip_comments:
        return list(filter(lambda post: post.get('com') == None or post.get('filename'), posts))
    if skip_files:
        return list(filter(lambda post: post.get('filename') == None, posts))
    else:
        return posts

@click.command()
@click.argument('thread')
@click.argument('webhook')
@click.option('--skip-comments', is_flag=True, default=False, help='Skips all comments')
@click.option('--skip-files', is_flag=True, default=False, help='Skips all comments containing files')
@click.option('--delay', type=click.INT, default=1, help='Delay to send webhooks', show_default=True)
def cmain(
    thread: str,
    webhook: str,
    skip_comments: bool,
    skip_files: bool,
    delay: int,
):
    thread_url = validate_thread_url(thread)
    webhook_url = validate_webhook_url(webhook)

    if thread_url['success'] == False:
        raise click.ClickException(f'{thread} is not a valid thread url')
    if webhook_url['success'] == False:
        raise click.ClickException(f'{webhook} is not a valid webhook url')

    wh = discord.SyncWebhook.from_url(webhook)

    thread_data = thread_url['result']
    r = requests.get(f'https://a.4cdn.org/{thread_data[2]}/thread/{thread_data[3]}.json')
    r.raise_for_status()
    js = r.json()

    posts = js['posts']
    thread_title = posts[0]['semantic_url']
    filtered = filter_posts(skip_comments=skip_comments, skip_files=skip_files, posts=posts)

    # map of thread number (no) to message (WebhookMessage)
    com_map: Dict[int, discord.SyncWebhookMessage] = {}

    for post in track(filtered):
        tim = post.get('tim')
        filename = post.get('filename')
        ext = post.get('ext')
        no = post['no']
        replyto = post.get('resto')

        # If the comment doesn't have an attachment
        if tim is None:
            com = post['com']
            # Check if the comment is a reply or not
            if replyto:
                # Hyperlinks don't work if either --skip-files or --skip-comments flag
                # is used because some comments may get skipped, so we don't hyperlink replies
                # because it has a chance of KeyError-ing when indexing `com_map`.
                if skip_comments or skip_files:
                    fmt = f'>>>{replyto}\n{normify_comment(com)}'[:2000]
                else:
                    replyto_hyperlink = f'[>>{replyto}]({com_map[replyto].jump_url})'
                    fmt = f'{replyto_hyperlink}{normify_comment(com)}'[:2000]

                sent = wh.send(
                    content=fmt,
                    username=f'{post["name"]} #{no}',
                    wait=True,
                    suppress_embeds=True
                )
            # If it reaches here, then it's a comment without a reply
            else:
                sent = wh.send(
                    content=str(post.get('com'))[:2000],
                    username=f'{post["name"]} #{no}',
                    wait=True,
                )
            com_map[no] = sent

        # If the comment has an attachment
        elif tim and filename and ext is not None:
            com = post.get('com')

            if com and replyto:
                fmt = f'>>>{replyto}\n{normify_comment(com)}'[:2000]
            elif com:
                fmt = f'{normify_comment(com)}'[:2000]
            else:
                fmt = ''

            sent = wh.send(
                content=fmt,
                username=f'{post["name"]} #{no}',
                file=construct_file(
                    board=thread_data[2],
                    tim=tim,
                    filename=filename,
                    ext=ext
                ),
                wait=True,
            )
            com_map[no] = sent

        time.sleep(delay)

if __name__ == '__main__':
    cmain()
import json
import os
import ssl

import certifi

from slack_sdk import WebClient

from .blocks import SlackMessageBlock


class SlackMessage:
    """
    A Slack message

    Args:
        *blocks: any child blocks
        token: the Slack token
        text: the message alternative text, shown if the message cannot
            be rendered by Slack

    """
    def __init__(
            self,
            *blocks,
            token: str = "",
            text: str = ""
    ):
        self.token = token if token else os.environ.get('SLACK_API_TOKEN')
        self.text = text
        self.blocks = blocks if blocks else []

    def send(self, channel: str = "") -> dict:
        """
        Send the message to Slack.

        Args:
            channel: the channel to send the message to
        """
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        client = WebClient(token=self.token, ssl=ssl_context)
        rendered_blocks = self.render()
        response = client.chat_postMessage(
            channel=channel,
            text=self.text,
            blocks=rendered_blocks
        )
        return response

    def add_block(self, block: SlackMessageBlock) -> None:
        """Add a block to the message."""
        self.blocks.append(block)

    def render(self) -> str:
        """Render the message content to JSON."""
        blocks = []
        for block in self.blocks:
            blocks.extend(block.render())
        return json.dumps(blocks)

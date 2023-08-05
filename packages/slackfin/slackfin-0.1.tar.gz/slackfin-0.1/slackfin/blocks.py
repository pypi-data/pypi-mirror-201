from .types import (
    SlackElementType,
    SlackImageType,
    SlackMarkdownType,
)


class SlackMessageBlock:
    """
    A Slack message block

    Args:
        *blocks: any child blocks
    """
    def __init__(self, *blocks):
        self.blocks = blocks if blocks else []

    def render(self) -> list:
        """Render the block to JSON."""
        blocks = []
        for block in self.blocks:
            blocks.extend(block.render())
        return blocks


class SlackMessageHeader(SlackMessageBlock):
    """
    A Slack message header

    Args:
        text: the header text
        emoji: whether to allow emojis

    """
    def __init__(
            self,
            *args,
            text: str = "",
            emoji: bool = True,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.text = text
        self.emoji = emoji

    def render(self) -> list:
        """Render the header to JSON."""
        blocks = super().render()
        segment = {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': self.text,
                'emoji': self.emoji
            }
        }
        blocks.append(segment)
        return blocks


class SlackMessageMarkdown(SlackMessageBlock):
    """
    A Slack message markdown

    Args:
        text: the markdown text
        image_url: the image URL
        alt_text: the alternative text

    """
    def __init__(
            self,
            *args,
            text: str = "",
            image_url: str = "",
            alt_text: str = "",
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.text = text
        if image_url:
            self.image = SlackImageType(image_url, alt_text)

    def render(self) -> list:
        """Render the markdown to JSON."""
        blocks = super().render()
        segment = {
            'type': 'section',
            'text': SlackMarkdownType(self.text).render()
        }
        if self.image:
            segment['accessory'] = self.image.render()
        blocks.append(segment)
        return blocks


class SlackLabelValuePair:
    """
    A label/value pair

    Args:
        label: the label
        value: the value
        label_url: the label URL
        value_url: the value URL

    """

    def __init__(
            self,
            label: str = "",
            value: str = "",
            label_url: str = "",
            value_url: str = ""
    ) -> None:
        self.label = label
        self.value = value
        self.label_url = label_url
        self.value_url = value_url

    def render(self) -> str:
        """Render the label/value pair to Markdown."""
        if self.label_url:
            label = f"<{self.label_url}|{self.label}>"
        else:
            label = self.label
        if self.value_url:
            value = f"<{self.value_url}|{self.value}>"
        else:
            value = self.value
        return f"*{label}*: {value}"


class SlackLabelValueListBlock(SlackMessageMarkdown):
    """
    A Slack message label/value list block

    Args:
        *entries: any SlackLabelValuePair entries

    """

    def __init__(self, *entries: SlackLabelValuePair, **kwargs):
        super().__init__(**kwargs)
        self.entries = entries if entries else []

    def add_entry(self, entry: SlackLabelValuePair) -> None:
        """Add an entry to the list."""
        self.entries.append(entry)

    def render(self) -> list:
        """Render the block to JSON."""
        joined = '\n'.join([entry.render() for entry in self.entries])
        self.text = f"{self.text}\n\n{joined}"
        return super().render()


class SlackMessageValueBlock(SlackMessageBlock):
    """
    A Slack message value block

    Args:
        label: the label
        value: the value
        secondary_label: the secondary label
        secondary_value: the secondary value
    """
    def __init__(
            self,
            *args,
            label: str = "",
            value: str = "",
            secondary_label: str = "",
            secondary_value: str = "",
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields = []
        self.fields.append({'type': 'mrkdwn', 'text': f"*{label}*\n{value}"})
        if secondary_label and secondary_value:
            self.fields.append(
                {
                    'type': 'mrkdwn',
                    'text': f"*{secondary_label}*\n{secondary_value}"
                }
            )

    def render(self) -> list:
        """Render the block to JSON."""
        blocks = super().render()
        segment = {
            'type': 'section',
            'fields': self.fields
        }
        blocks.append(segment)
        return blocks


class SlackMessageDivider(SlackMessageBlock):
    """
    A Slack message divider
    """

    def render(self) -> list:
        """Render the divider to JSON."""
        blocks = super().render()
        segment = {
            'type': 'divider'
        }
        blocks.append(segment)
        return blocks


class SlackMessageContext(SlackMessageBlock):
    """
    A Slack message context

    Args:
        *elements: any SlackElementType elements
    """
    def __init__(self, *elements: SlackElementType, **kwargs):
        super().__init__(**kwargs)
        self.elements = elements if elements else []

    def add_element(self, element: SlackElementType) -> None:
        """Add an element to the context."""
        self.elements.append(element)

    def render(self) -> list:
        """Render the context to JSON."""
        blocks = super().render()
        elements = []
        for element in self.elements:
            elements.append(element.render())
        segment = {
            'type': 'context',
            'elements': elements
        }
        blocks.append(segment)
        return blocks

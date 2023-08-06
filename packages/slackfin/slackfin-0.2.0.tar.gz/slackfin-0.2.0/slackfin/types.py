

class SlackElementType:
    """A Slack element."""
    def __init__(self, element_type: str = None):
        self.data = {
            "type": element_type
        }

    def add_value(self, key: str, value: str):
        """Add a value to the element."""
        self.data[key] = value

    def render(self) -> dict:
        """Render the element to JSON."""
        return self.data


class SlackPlainTextType(SlackElementType):
    """A Slack plain text type."""
    def __init__(self, text: str = "", emoji: bool = True):
        super().__init__(element_type='plain_text')
        self.add_value("text", text)
        self.add_value("emoji", emoji)
        self.text = text


class SlackMarkdownType(SlackElementType):
    """A Slack markdown text type."""
    def __init__(self, text: str = ""):
        super().__init__(element_type='mrkdwn')
        if not isinstance(text, str):
            text = str(text)
        self.add_value("text", text)
        self.text = text


class SlackImageType(SlackElementType):
    """A Slack image type."""
    def __init__(self, image_url: str = "", alt_text: str = ""):
        super().__init__(element_type='image')
        self.add_value("image_url", image_url)
        self.add_value("alt_text", alt_text)

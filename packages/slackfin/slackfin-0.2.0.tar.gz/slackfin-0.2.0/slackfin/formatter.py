from datetime import datetime


class SlackFormatter:
    """
    SlackFormatter

    Slack formats a number of things in a special way. This class provides
    methods to format those things.
    """

    def datetime(
        self,
        timestamp: datetime = None,
        date_format: str = "{date_num} {time}",
        url: str = None,
    ):
        """Format a datetime object into a Slack date string."""

        if not timestamp:
            timestamp = datetime.now()
        formatted_string = f"<!date^{int(timestamp.timestamp())}^{date_format}"
        if url:
            formatted_string += f"^{url}"
        formatted_string += f"|{str(timestamp)}>"
        return formatted_string

    def link(
            self, url: str,
            text: str = None
        ):
        """Format a URL into a Slack link."""
        return f"<{url}|{text if text else url}>"

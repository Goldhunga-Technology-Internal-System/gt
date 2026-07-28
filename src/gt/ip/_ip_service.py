from dataclasses import dataclass
from typing import TypedDict

from fastapi.requests import Request


class ParsedUserAgent(TypedDict):
    device: str
    browser: str
    os: str


@dataclass(slots=True, frozen=True)
class IPContext:
    """Represents the context of an IP address in a request."""

    ip_address: str
    device: str
    browser: str
    os: str


class IPService:
    """
    Service class for handling IP-related operations.
    """

    @staticmethod
    def get_ip_context(request: Request) -> IPContext:
        """
        Retrieve the IP context.

        Returns:
            The IPContext instance.
        """
        ip_address = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        parsed = IPService.parse_user_agent(user_agent)

        return IPContext(
            ip_address=ip_address,
            device=parsed["device"],
            browser=parsed["browser"],
            os=parsed["os"],
        )

    @staticmethod
    def parse_user_agent(user_agent: str) -> ParsedUserAgent:
        """
        Parse the user agent string to extract device, browser, and OS information.

        Args:
            user_agent: The user agent string from the request headers.
        """
        import user_agents

        ua = user_agents.parse(user_agent)
        browser = f"{ua.browser.family} {ua.browser.version_string}"
        device = f"{ua.device.family}"
        os = f"{ua.os.family} {ua.os.version_string}"

        return ParsedUserAgent(device=device, browser=browser, os=os)

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.message import Message
    from aiva.core.utils.classes.message_instances import MessageInstances
    from aiva.core.utils.classes.payload import Payload
    from aiva.core.utils.enums.role import Role


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHATBOT
# └─────────────────────────────────────────────────────────────────────────────────────


class Chatbot(ABC):
    """A utility class that normalizes functionality across chatbot APIs"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize name
    NAME: str = ""

    # Initialize keys to None
    KEYS: tuple[str, ...] = ()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, api_key: str, **kwargs: Kwargs):
        """Init Method"""

        # Set API key
        self.api_key = api_key

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE MESSAGE
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def create_message(
        self, text: str, role: Role, role_name: str | None = None, **kwargs: Kwargs
    ) -> Message:
        """Initializes and returns a Message instance for the API"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE REQUEST PAYLOAD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def create_request_payload(
        self,
        prompt: Message,
        message: Message,
        history: MessageInstances,
        **kwargs: Kwargs,
    ) -> Payload:
        """Initializes and returns a Payload instance for the API request"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE RESPONSE PAYLOAD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def create_response_payload(self, **kwargs: Kwargs) -> Payload:
        """Initializes and returns a Payload instance for the API response"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def send(
        self, payload: Payload, **kwargs: Kwargs
    ) -> Generator[Message, None, None]:
        """Sends a payload to the API synchronously and yields Message instances"""

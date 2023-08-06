# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.message_instances import MessageInstances


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PAYLOAD
# └─────────────────────────────────────────────────────────────────────────────────────


class Payload:
    """A utility class that represents the payload of a Request / Response instance"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of token count
    _token_count: int

    # Declare type of token limit
    token_limit: int | None

    # Declare type of messages
    messages: MessageInstances

    # Declare type of data
    data: dict[str, Any]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        token_count: int = 0,
        token_limit: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Init Method"""

        # Set token count
        self._token_count = token_count

        # Set token limit
        self.token_limit = token_limit

        # Initialize and set messages
        self.messages = MessageInstances()

        # Set data
        self.data = data or {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RESPECTS TOKEN LIMIT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def respects_token_limit(self) -> bool:
        """Returns whether the token count respects the token limit"""

        # Return True if token limit is None
        if self.token_limit is None:
            return True

        # Return whether the token count respects the token limit
        return self.token_count <= self.token_limit

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TOKEN COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def token_count(self) -> int:
        """Returns the token count of the current Payload instance and its messages"""

        # Initialize token count
        token_count = self._token_count

        # Increment token count by message token counts
        token_count += self.messages.token_count

        # Return token count
        return token_count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TO JSON
    # └─────────────────────────────────────────────────────────────────────────────────

    def to_json(self, messages_key: str = "messages") -> dict[str, Any]:
        """Converts the Payload instance to JSON"""

        # Get data
        data = self.data

        # Get message list
        message_list = self.messages.to_json()

        # Add message list to data
        data[messages_key] = message_list

        # Return dictionary
        return data

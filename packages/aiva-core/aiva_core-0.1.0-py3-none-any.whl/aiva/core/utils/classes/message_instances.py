# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.types import Kwargs
from aiva.core.utils.classes.message import Message
from aiva.core.utils.mixins.instances import Instances


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ MESSAGE INSTANCES
# └─────────────────────────────────────────────────────────────────────────────────────


class MessageInstances(Instances[Message]):
    """A utility class to represent a collection of Message instances"""

    # Declare type of token count
    _token_count: int

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, token_count: int = 0, **kwargs: Kwargs) -> None:
        """Init Method"""

        # Call super method
        super().__init__(**kwargs)

        # Set token count
        self._token_count = token_count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TOKEN COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def token_count(self) -> int:
        """Returns the token count of all Message instances"""

        # Initialize token count
        token_count = self._token_count

        # Increment token count by message token counts
        token_count += sum(message.token_count for message in self)

        # Return token count
        return token_count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, tokens: int) -> MessageInstances:
        """Returns a the last n Message instances worth of tokens"""

        # Initialize remaining tokens
        remaining_tokens = tokens

        # Initialize messages
        messages = []

        # Iterate over messages in reverse
        for message in reversed(list(self)):
            # Break if message token count is greater than remaining tokens
            if message.token_count > remaining_tokens:
                break

            # Append message to messages
            messages.append(message)

        # Initialize tail
        tail = MessageInstances()

        # Iterate over messages in reverse
        for message in reversed(messages):
            # Add message to tail
            tail.add(message)

        # Return tail
        return tail

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TO JSON
    # └─────────────────────────────────────────────────────────────────────────────────

    def to_json(self) -> list[dict[str, Any]]:
        """Converts the collection of Message instances to JSON"""

        # Return messages
        return [message.to_json() for message in self]

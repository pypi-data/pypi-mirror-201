# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.exceptions import AlreadySentError
from aiva.core.utils.classes.request import Request
from aiva.core.utils.classes.response import Response

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.chat import Chat
    from aiva.core.utils.classes.message import Message


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRANSACTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Transaction:
    """A utility class that normalizes transactions within Chat instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of chat
    chat: Chat

    # Declare type of request
    request: Request

    # Declare type of response
    response: Response

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, chat: Chat, message: str) -> None:
        """Init Method"""

        # Set chat
        self.chat = chat

        # Initialize and set request
        self.request = Request(transaction=self, message=message)

        # Initialize and set response
        self.response = Response(transaction=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ IS COMPLETE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def is_complete(self) -> bool:
        """Returns a boolean indicating whether the transaction is complete"""

        # Return boolean indicating whether the transaction is complete
        return self.request.is_complete and self.response.is_complete

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def send(self, **kwargs: Kwargs) -> Generator[Message, None, None]:
        """Sends a synchronous transaction request and yields Message instances"""

        # Check if the transaction is already complete
        if self.is_complete:
            # Raise AlreadySentError
            raise AlreadySentError("This transaction has already been sent.")

        # Send request and yield Message instances
        for message in self.request.send(**kwargs):
            # Mark request as complete
            self.request.is_complete = True

            # Receive and yield message
            yield self.response.receive(message)

        # Mark response as complete
        self.response.is_complete = True

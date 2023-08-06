# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.message import Message
from aiva.core.utils.classes.payload import Payload
from aiva.core.utils.enums.role import Role

if TYPE_CHECKING:
    from aiva.core.utils.classes.chat import Chat
    from aiva.core.utils.classes.chatbot import Chatbot
    from aiva.core.utils.classes.transaction import Transaction


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ RESPONSE
# └─────────────────────────────────────────────────────────────────────────────────────


class Response:
    """A utility class that normalizes transaction responses across chatbot APIs"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of transaction
    transaction: Transaction

    # Declare type of payload
    payload: Payload

    # Declare type of is complete
    is_complete: bool

    # Declare type of message
    _message: Message | None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, transaction: Transaction) -> None:
        """Init Method"""

        # Set transaction
        self.transaction = transaction

        # Initialize and set payload
        self.payload = Payload()

        # Initialize is complete to False
        self.is_complete = False

        # Initialize cached message to None
        self._message = None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CHAT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def chat(self) -> Chat:
        """Returns the Chat instance associated with the Response instance"""

        # Return the Chat instance
        return self.transaction.chat

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CHATBOT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def chatbot(self) -> Chatbot:
        """Returns the Chatbot instance associated with the Response instance"""

        # Return the Chatbot instance
        return self.chat.bot

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ MESSAGE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def message(self) -> Message:
        """Returns the Message instance associated with the Response instance"""

        # Get message
        _message = self._message

        # Check if message is None
        if _message is None:
            # Initialize message text
            text = ""

            # Iterate over messages
            for message in self.payload.messages:
                # Update message text
                text += message.text

            # Strip message text
            text = text.strip()

            # Initialize a new Message instance
            _message = self.chatbot.create_message(text=text, role=Role.ASSISTANT)

            # Check if the response is complete
            if self.is_complete:
                # Cache the Message instance
                self._message = _message

        # Return Message instance
        return _message

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RECEIVE
    # └─────────────────────────────────────────────────────────────────────────────────

    def receive(self, message: Message) -> Message:
        """Receives and returns a Message instance"""

        # Add the Message instance to payload messages
        self.payload.messages.add(message)

        # Return Message instance
        return message

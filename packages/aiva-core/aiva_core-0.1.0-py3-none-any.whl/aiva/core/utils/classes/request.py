# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.exceptions import AlreadySentError, TokenLimitExceededError
from aiva.core.utils.classes.chatbot import Chatbot
from aiva.core.utils.classes.message import Message
from aiva.core.utils.classes.payload import Payload
from aiva.core.utils.classes.message_instances import MessageInstances
from aiva.core.utils.enums.role import Role

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.chat import Chat
    from aiva.core.utils.classes.response import Response
    from aiva.core.utils.classes.transaction import Transaction


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ REQUEST
# └─────────────────────────────────────────────────────────────────────────────────────


class Request:
    """A utility class that normalizes transaction requests across chatbot APIs"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of transaction
    transaction: Transaction

    # Declare type of message
    message: Message

    # Declare type of payload
    payload: Payload

    # Declare type of is complete
    is_complete: bool

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, transaction: Transaction, message: str) -> None:
        """Init Method"""

        # Set transaction
        self.transaction = transaction

        # Initialize and set message
        self.message = Message(text=message, role=Role.USER, role_name=None)

        # Initialize and set payload
        self.payload = Payload()

        # Initialize is complete to False
        self.is_complete = False

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CHAT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def chat(self) -> Chat:
        """Returns the Chat instance associated with the Request instance"""

        # Return the Chat instance
        return self.transaction.chat

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CHATBOT
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def chatbot(self) -> Chatbot:
        """Returns the Chatbot instance associated with the Request instance"""

        # Return the Chatbot instance
        return self.chat.bot

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ RESPONSE
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def response(self) -> Response:
        """Returns the ChatResponse instance associated with the Request instance"""

        # Return the ChatResponse instance
        return self.transaction.response

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def send(self, **kwargs: Kwargs) -> Generator[Message, None, None]:
        """Sends a synchronous request and yields Message instances"""

        # Return request if is already complete
        if self.is_complete:
            # Raise AlreadySentError
            raise AlreadySentError("This request has already been sent.")

        # Get chat
        chat = self.chat

        # Get chatbot
        chatbot = chat.bot

        # Get prompt
        prompt = chatbot.create_message(
            text=chat.assistant.PROMPT, role=Role.SYSTEM, role_name=None, **kwargs
        )

        # Initialize chat history
        history = MessageInstances()

        # Iterate over chat history
        for message in chat.history:
            # Create and append a new Message instance to history
            history.add(
                chatbot.create_message(
                    text=message.text,
                    role=message.role,
                    role_name=message.role_name,
                    **kwargs,
                )
            )

        # Initialize and set a new Message instance
        message = self.message = chatbot.create_message(
            text=self.message.text,
            role=self.message.role,
            role_name=self.message.role_name,
            **kwargs,
        )

        # Initialize and set payload
        payload = self.payload = chatbot.create_request_payload(
            prompt=prompt, message=message, history=history, **kwargs
        )

        # Check if payload does not respect token limit
        if not payload.respects_token_limit:
            # Raise TokenLimitExceededError
            raise TokenLimitExceededError(
                f"Request payload exceeds token limit of {self.payload.token_limit}"
            )

        # Yield Message instances
        yield from chatbot.send(payload=payload, **kwargs)

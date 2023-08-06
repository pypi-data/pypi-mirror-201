# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.chatbot import Chatbot
from aiva.core.utils.classes.message import Message
from aiva.core.utils.classes.message_instances import MessageInstances
from aiva.core.utils.classes.transaction import Transaction
from aiva.core.utils.classes.transaction_instances import TransactionInstances

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.assistant import Assistant


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHAT
# └─────────────────────────────────────────────────────────────────────────────────────


class Chat:
    """A utility class for managing individual chats threads for a given Chatbot"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of assistant
    assistant: Assistant

    # Declare type of bot
    bot: Chatbot

    # Declare type of transactions
    transactions: TransactionInstances

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, assistant: Assistant, bot: Chatbot) -> None:
        """Init Method"""

        # Set assistant
        self.assistant = assistant

        # Set bot
        self.bot = bot

        # Initialize and set transactions
        self.transactions = TransactionInstances()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HISTORY
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def history(self) -> MessageInstances:
        """Returns a collection of Message instances in the current Chat instance"""

        # Initialize history
        history = MessageInstances()

        # Iterate over transactions
        for transaction in self.transactions:
            # Get request
            request = transaction.request

            # Continue if request is not complete
            if not request.is_complete:
                continue

            # Add request message to history
            history.add(request.message)

            # Get response
            response = transaction.response

            # Check if response is complete
            if response.is_complete:
                # Add response message to history
                history.add(response.message)

        # Return history
        return history

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def send(self, message: str, **kwargs: Kwargs) -> Generator[Message, None, None]:
        """Sends a synchronous Transaction and yields Message instances"""

        # Initialize Transaction instance
        transaction = Transaction(chat=self, message=message)

        # Add Transaction instance to transactions
        self.transactions.add(transaction)

        # Iterate over Message instances
        yield from transaction.send(**kwargs)

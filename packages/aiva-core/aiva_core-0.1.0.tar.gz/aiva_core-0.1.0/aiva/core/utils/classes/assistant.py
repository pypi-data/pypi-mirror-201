# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.chat import Chat
from aiva.core.utils.classes.chat_instances import ChatInstances
from aiva.core.utils.classes.chatbot_classes import ChatbotClasses

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.chatbot import Chatbot
    from aiva.core.utils.classes.message import Message


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ASSISTANT
# └─────────────────────────────────────────────────────────────────────────────────────


class Assistant:
    """A utility class that represents an chatbot-driven AI assistant"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize a default assistant prompt
    PROMPT: str = "You are a helpful AI assistant."

    # Initialize Chatbot classes
    CHATBOT_CLASSES: tuple[type[Chatbot], ...] = ()

    # Declare type of this chat
    this_chat: Chat

    # Declare type of all chats
    all_chats: ChatInstances

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, chatbot: str, chatbot_api_key: str = "") -> None:
        """Init Method"""

        # Initialize Chatbot classes
        chatbot_classes = ChatbotClasses()

        # Iterate over Chatbot classes
        for ChatbotClass in self.CHATBOT_CLASSES:
            # Register Chatbot class
            chatbot_classes.register(ChatbotClass=ChatbotClass)

        # Initialize Chatbot instance
        bot = chatbot_classes.initialize(key=chatbot, api_key=chatbot_api_key)

        # Initialize and set this chat
        self.this_chat = Chat(assistant=self, bot=bot)

        # Initialize and set all chats
        self.all_chats = ChatInstances()

        # Add this chat to all chats
        self.all_chats.add(self.this_chat)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def send(self, message: str, **kwargs: Kwargs) -> Generator[Message, None, None]:
        """Initiates a Transaction and yields Message instances"""

        # Yield Message instances
        yield from self.this_chat.send(message=message, **kwargs)

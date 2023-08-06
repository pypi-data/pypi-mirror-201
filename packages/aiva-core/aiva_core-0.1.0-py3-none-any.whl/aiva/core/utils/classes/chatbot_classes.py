# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.exceptions import DuplicateChatbotKeyError, UnsupportedChatbotError

if TYPE_CHECKING:
    from aiva.core.utils.classes.chatbot import Chatbot


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHATBOT CLASSES
# └─────────────────────────────────────────────────────────────────────────────────────


class ChatbotClasses:
    """A utility class that represents a collection of Chatbot classes"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of classes by key
    _classes_by_key: dict[str, type[Chatbot]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize classes by key
        self._classes_by_key = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _NORMALIZE KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def _normalize_key(self, key: str) -> str:
        """Normalizes a Chatbot class key"""

        # Strip key
        key = key.strip()

        # Lowercase key
        key = key.lower()

        # Remove non-alphanumeric characters from key
        key = "".join([char for char in key if char.isalnum()])

        # Return normalized key
        return key

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INITIALIZE
    # └─────────────────────────────────────────────────────────────────────────────────

    def initialize(self, key: str, api_key: str) -> Chatbot:
        """Initialize a Chatbot instance given a key"""

        # Normalize key
        key_normalized = self._normalize_key(key)

        # Check if key does not exist
        if key_normalized not in self._classes_by_key:
            # Raise UnsupportedChatbotError
            raise UnsupportedChatbotError(f"The chatbot '{key}' is not supported.")

        # Get Chatbot class
        ChatbotClass = self._classes_by_key[key_normalized]

        # Initialize Chatbot instance
        chatbot = ChatbotClass(api_key)

        # Return Chatbot instance
        return chatbot

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ REGISTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def register(self, ChatbotClass: type[Chatbot]) -> None:
        """Registers a Chatbot class"""

        # Get KEYS
        KEYS = ChatbotClass.KEYS

        # Initialize normalized keys
        keys_normalized: set[str] = set()

        # Iterate over keys
        for key in KEYS:
            # Normalize key
            key_normalized = self._normalize_key(key)

            # Check if Chatbot class is already registered
            if key_normalized in self._classes_by_key:
                # Ignore if Chatbot class is the same
                if self._classes_by_key[key_normalized] is ChatbotClass:
                    continue

                # Raise DuplicateChatbotKeyError
                raise DuplicateChatbotKeyError(
                    f"A Chatbot class with the key '{key}' "
                    f"(normalized: {key_normalized}) already exists."
                )

            # Add normalized key to normalized keys
            keys_normalized.add(key_normalized)

        # Add Chatbot class to classes by key
        self._classes_by_key.update({key: ChatbotClass for key in keys_normalized})

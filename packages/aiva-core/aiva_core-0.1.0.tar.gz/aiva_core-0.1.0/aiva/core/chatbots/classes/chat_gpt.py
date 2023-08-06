# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

import logging
import tiktoken

from decimal import Decimal
from openai import ChatCompletion
from typing import Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.chatbot import Chatbot
from aiva.core.utils.classes.message import Message
from aiva.core.utils.classes.payload import Payload
from aiva.core.utils.enums.role import Role

if TYPE_CHECKING:
    from aiva.core.types import Kwargs
    from aiva.core.utils.classes.message_instances import MessageInstances


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHAT GPT
# └─────────────────────────────────────────────────────────────────────────────────────


class ChatGPT(Chatbot):
    """An Chatbot class for interfacing with OpenAI's ChatGPT API"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define name
    NAME = "ChatGPT"

    # Define keys
    KEYS = ("chat gpt", "chat-gpt", "chat_gpt", "chatgpt", "gpt", "openai")

    # Define model
    MODEL = "gpt-3.5-turbo"

    # Define model encoding
    MODEL_ENCODING = tiktoken.encoding_for_model(MODEL)

    # Define stream
    STREAM = True

    # Define temperature
    TEMPERATURE = 0.8

    # Define token limit
    TOKEN_LIMIT = 4096

    # Define response token info
    TOKENS_FOR_RESPONSE = 500  # Number of tokens available for response
    TOKENS_PER_RESPONSE = 3  # Primed: <|start|>{role/name}<|message|>

    # Define request token info
    TOKENS_PER_REQUEST_MESSAGE = 4  # Primed: <im_start>{role/name}\n{content}<im_end>\n
    TOKENS_PER_REQUEST_MESSAGE_NAME = -1  # Role is omitted if there is a name

    # Define USD cost per token
    COST_USD_PER_TOKEN = Decimal("0.002") / Decimal("1000")

    # See https://github.com/openai/openai-cookbook/
    # blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT MESSAGE TOKENS
    # └─────────────────────────────────────────────────────────────────────────────────

    def count_message_data_tokens(
        self, message_data: dict[str, str], **kwargs: Kwargs
    ) -> int:
        """Computes and returns the estimated token count of a message data object"""

        # Initialize token count
        token_count = self.TOKENS_PER_REQUEST_MESSAGE

        # Iterate over message items
        for key, text in message_data.items():
            # Increment token count by text token count
            token_count += self.count_text_tokens(text)

            # Check if key is name
            if key == "name":
                # Increment token count by tokens per name
                token_count += self.TOKENS_PER_REQUEST_MESSAGE_NAME

        # Return token count
        return token_count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT TEXT TOKENS
    # └─────────────────────────────────────────────────────────────────────────────────

    def count_text_tokens(self, text: str) -> int:
        """Computes and returns the estimated token count of a string"""

        # Encode text
        encoded_text = self.MODEL_ENCODING.encode(text)

        # Get token count
        token_count = len(encoded_text)

        # Return token count of message
        return token_count

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE MESSAGE
    # └─────────────────────────────────────────────────────────────────────────────────

    def create_message(
        self,
        text: str,
        role: Role,
        role_name: str | None = None,
        text_only: bool = False,
        **kwargs: Kwargs,
    ) -> Message:
        """Initializes and returns a Message instance for the API"""

        # Define roles
        roles = {
            Role.ASSISTANT: "assistant",
            Role.SYSTEM: "system",
            Role.USER: "user",
        }

        # Check if role not in roles
        if role not in roles:
            # Emit warning
            logging.warning(f"Role '{role}' not explicitly handled by {self.NAME}.")

            # Set role name
            role_name = role.value

            # Set role
            role = Role.SYSTEM

        # Initialize message data
        data = {
            "role": roles[role],
            **({"name": role_name} if role_name else {}),
            "content": text,
        }

        # Get token count
        token_count = (
            self.count_text_tokens(text)
            if text_only
            else self.count_message_data_tokens(message_data=data)
        )

        # Initialize Message instance
        message = Message(
            text=text,
            role=role,
            role_name=role_name,
            token_count=token_count,
            data=data,
        )

        # Return Message instance
        return message

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE REQUEST PAYLOAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def create_request_payload(
        self,
        prompt: Message,
        message: Message,
        history: MessageInstances,
        stream: bool | None = None,
        temperature: float | None = None,
        **kwargs: Kwargs,
    ) -> Payload:
        """Initializes and returns a Payload instance for the API request"""

        # Get tokens for response
        TOKENS_FOR_RESPONSE = self.TOKENS_FOR_RESPONSE

        # Get tokens per response
        TOKENS_PER_RESPONSE = self.TOKENS_PER_RESPONSE

        # Compute token limit
        token_limit = self.TOKEN_LIMIT - TOKENS_PER_RESPONSE - TOKENS_FOR_RESPONSE

        # Get stream
        stream = stream if stream is not None else self.STREAM

        # Get temperature
        temperature = temperature if temperature is not None else self.TEMPERATURE

        # Initialize payload data
        data = {
            "api_key": self.api_key,
            "model": self.MODEL,
            "temperature": temperature,
            "max_tokens": TOKENS_FOR_RESPONSE,
            "stream": stream,
        }

        # Get token count
        token_count = TOKENS_PER_RESPONSE

        # Initialize Payload instance
        payload = Payload(token_count=token_count, token_limit=token_limit, data=data)

        # Initialize remaining tokens
        remaining_tokens = token_limit - prompt.token_count - message.token_count

        # Get tail of history
        history_tail = history.tail(tokens=remaining_tokens)

        # Add prompt to payload messages
        payload.messages.add(prompt)

        # Add tail of history to payload messages
        payload.messages.add(history_tail)

        # Add message to payload messages
        payload.messages.add(message)

        # Return Payload instance
        return payload

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE RESPONSE PAYLOAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def create_response_payload(self, **kwargs: Kwargs) -> Payload:
        """Initializes and returns a Payload instance for the API response"""

        # Get token count
        token_count = 0

        # Get token limit
        token_limit = self.TOKENS_FOR_RESPONSE

        # Initialize Payload instance
        payload = Payload(token_count=token_count, token_limit=token_limit)

        # Return Payload instance
        return payload

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def send(
        self, payload: Payload, **kwargs: Kwargs
    ) -> Generator[Message, None, None]:
        """Sends a payload to the API synchronously and yields Message instances"""

        # Make API request
        messages = ChatCompletion.create(**payload.to_json())  # type: ignore

        # Initialize choice key
        message_key = "delta"

        # Check if messages is a dictionary
        if isinstance(messages, dict):
            # Ensure that messages is a list
            messages = [messages]

            # Set choice key to message
            message_key = "message"

        # Initialize is first message to True
        is_first_message = True

        # Iterate over messages
        for message in messages:
            # Get choices
            choices = message["choices"]

            # Get choice
            choice = choices[0]

            # Get choice message
            choice_message = choice[message_key]

            # Continue if content not in choice message
            if "content" not in choice_message:
                continue

            # Extract message text
            message_text = choice_message["content"]

            # Check if is first message
            if is_first_message:
                # Left strip message text
                message_text = message_text.lstrip()

            # Initialize ResponseMessage instance
            response_message = self.create_message(
                text=message_text, role=Role.ASSISTANT, text_only=True
            )

            # Yield ResponseMessage instance
            yield response_message

            # Set is first message to False
            is_first_message = False

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DUPLICATE CHATBOT KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class DuplicateChatbotKeyError(Exception):
    """An exception raised when a registered Chatbot class key is not unique"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ALREADY SENT ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class AlreadySentError(Exception):
    """An exception raised when a transaction has already been sent"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TOKEN LIMIT EXCEEDED ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class TokenLimitExceededError(Exception):
    """An exception raised when a token limit is exceeded"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNSUPPORTED CHATBOT ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UnsupportedChatbotError(Exception):
    """An exception raised when a Chatbot class is not supported"""

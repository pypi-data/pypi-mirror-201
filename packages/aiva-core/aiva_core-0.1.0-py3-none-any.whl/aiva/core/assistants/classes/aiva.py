# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.chatbots.classes.chat_gpt import ChatGPT
from aiva.core.utils.classes.assistant import Assistant


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ AIVA
# └─────────────────────────────────────────────────────────────────────────────────────


class AIVA(Assistant):
    """A class that defines the core functionality of AIVA, the AI Virtual Assistant"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define a prompt for AIVA
    PROMPT = "You are AIVA, a quirky but helpful AI Virtual Assistant."

    # Initialize Chatbot classe
    CHATBOT_CLASSES = (ChatGPT,)

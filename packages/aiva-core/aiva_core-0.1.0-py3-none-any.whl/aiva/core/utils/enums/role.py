# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from enum import Enum


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ROLE
# └─────────────────────────────────────────────────────────────────────────────────────


class Role(Enum):
    """An enumeration of the roles that a Message instance can have"""

    # Define assistant role
    ASSISTANT = "assistant"

    # Define system role
    SYSTEM = "system"

    # Define user role
    USER = "user"

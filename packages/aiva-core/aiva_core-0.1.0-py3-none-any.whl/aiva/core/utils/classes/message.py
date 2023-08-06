# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.enums.role import Role


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ MESSAGE
# └─────────────────────────────────────────────────────────────────────────────────────


class Message:
    """A utility class that represents messages"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of text
    text: str

    # Declare type of role
    role: Role

    # Declare type of role name
    role_name: str | None

    # Declare type of token count
    token_count: int

    # Declare type of data
    data: dict[str, Any]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        text: str,
        role: Role,
        role_name: str | None = None,
        token_count: int = 0,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Init Method"""

        # Set text
        self.text = text

        # Set role
        self.role = role

        # Set role name
        self.role_name = role_name

        # Set token count
        self.token_count = token_count

        # Set data
        self.data = data or {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TO JSON
    # └─────────────────────────────────────────────────────────────────────────────────

    def to_json(self) -> dict[str, Any]:
        """Convert the message to JSON"""

        # Get message data
        data = self.data or {
            "text": self.text,
            "role": self.role.value,
            **({"role_name": self.role_name} if self.role_name else {}),
        }

        # Return message data
        return data

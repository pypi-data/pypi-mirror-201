# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.chat import Chat
from aiva.core.utils.mixins.instances import Instances


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CHAT INSTANCES
# └─────────────────────────────────────────────────────────────────────────────────────


class ChatInstances(Instances[Chat]):
    """A utility class to represent a collection of Chat instances"""

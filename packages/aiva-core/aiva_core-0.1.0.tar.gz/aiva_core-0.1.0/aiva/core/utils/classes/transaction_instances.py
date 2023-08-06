# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from aiva.core.utils.classes.transaction import Transaction
from aiva.core.utils.mixins.instances import Instances


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ TRANSACTION INSTANCES
# └─────────────────────────────────────────────────────────────────────────────────────


class TransactionInstances(Instances[Transaction]):
    """A utility class to represent a collection of Transaction instances"""

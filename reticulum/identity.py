"""
RServer identity management.
"""

import os
import RNS
import config


def get_or_create_identity():
    """Load existing identity or create a new one. Returns (identity, was_created)."""

    identity_file = config.identity_path()
    
    if os.path.exists(identity_file):
        return load_identity(identity_file), False
    else:
        return create_identity(identity_file), True


def load_identity(identity_file):
    """Load an existing identity from file."""

    identity = RNS.Identity.from_file(identity_file)
    if identity is None:
        raise ValueError(f"Invalid identity file at {identity_file}. Please delete the corrupted file and restart.")
    return identity


def create_identity(identity_file):
    """Create a new identity and save it to file."""

    identity = RNS.Identity()
    os.makedirs("config", exist_ok=True)
    identity.to_file(identity_file)
    return identity

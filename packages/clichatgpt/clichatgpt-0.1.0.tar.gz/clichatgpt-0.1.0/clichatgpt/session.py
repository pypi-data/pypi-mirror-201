import os
import re
import glob
from . import storage


def list():
    """List names of sessions."""
    sess_paths = glob.glob(os.path.join(storage.get_cache_path(), "*.yaml"))

    return sorted(
        [
            re.sub("\.yaml\Z", "", os.path.basename(sess_path))  # noqa: W605
            for sess_path in sess_paths
        ]
    )


def delete(session):
    """Deletes a session.
    Returns None on success, error string otherwise"""
    session_path = storage.get_session_path(session, True)
    if not session_path:
        return f"session {session} does not exist"

    os.unlink(session_path)


def rename(session, newname):
    """Renames session.
    Returns None on success, error string otherwise"""
    session_path = storage.get_session_path(session, True)
    if not session_path:
        return f"session {session} does not exist"

    new_session_path = storage.get_session_path(newname, True)
    if new_session_path:
        return f"session {newname} already exists"

    new_session_path = storage.get_session_path(newname)

    os.rename(session_path, new_session_path)

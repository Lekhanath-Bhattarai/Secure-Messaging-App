import shutil
import os
from core.user_management import register_user, get_keys

def test_register_user():
    username = "testuser"
    user_dir = f"data/users/{username}"
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
    success, msg = register_user(username)
    assert success
    private, public = get_keys(username)
    assert private is not None
    assert public is not None

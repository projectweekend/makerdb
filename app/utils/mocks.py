from app.user.data import DuplicateUserError


def mock_add_user(user):
    return


def mock_add_user_fail(user):
    raise DuplicateUserError

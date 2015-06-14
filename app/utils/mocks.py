from app.user.data import DuplicateUserError


def mock_add_user(user):
    return


def mock_add_user_fail(user):
    raise DuplicateUserError


def mock_find_user(email):
    return {
        'email': email,
        'account_type': 'user',
        'password': '$2a$12$exQfW2E2srRwMQFyBAL5l.MgDlfmEhPUjIP3izGJlhrx2R/dgBZoC'
    }


def mock_find_user_not_exists(email):
    return None

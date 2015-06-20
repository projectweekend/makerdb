from uuid import uuid4
from app.user.data import DuplicateUserError
from app.inventory_item.data import DuplicateUserInventoryItemError


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


def mock_add_user_inventory_item(user_email, user_item):
    return {
        'id': str(uuid4()),
        'user_email': user_email,
        'name': 'Super Cool Thing',
        'url': '',
        'image_url': '',
        'quantity': 1,
        'vendor_item_id': '',
        'vendor_name': '',
        'vendor_site': ''
    }


def mock_add_user_inventory_item_fail(user_email, user_item):
    raise DuplicateUserInventoryItemError


def mock_list_user_inventory_items(user_email):
    return [
        {
            'id': str(uuid4()),
            'user_email': user_email,
            'name': 'Super Cool Thing',
            'url': '',
            'image_url': '',
            'quantity': 1,
            'vendor_item_id': '',
            'vendor_name': '',
            'vendor_site': ''
        }
    ]


def mock_find_user_inventory_item(user_email, user_item_id):
    return {
        'id': user_item_id,
        'user_email': user_email,
        'name': 'Super Cool Thing',
        'url': '',
        'image_url': '',
        'quantity': 1,
        'vendor_item_id': '',
        'vendor_name': '',
        'vendor_site': ''
    }


def mock_find_user_inventory_item_not_exists(user_email, user_item_id):
    return []

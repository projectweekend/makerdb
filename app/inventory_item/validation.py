from app.utils.validation import BaseValidationMixin


class InventoryItemValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'image_url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'quantity': {
            'type': 'integer',
            'required': True
        },
        'vendor_name': {
            'type': 'string',
            'required': True,
            'empty': True
        },
        'vendor_item_id': {
            'type': 'string',
            'required': True,
            'empty': True
        }
    }

    schema_for_put = {
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'image_url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'quantity': {
            'type': 'integer',
            'required': True
        },
        'vendor_name': {
            'type': 'string',
            'required': True,
            'empty': True
        },
        'vendor_item_id': {
            'type': 'string',
            'required': True,
            'empty': True
        }
    }

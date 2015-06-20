from app.utils.validation import BaseValidationMixin


class InventoryItemCreateMixin(BaseValidationMixin):

    schema = {
        'item_name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'item_url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'item_image_url': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        },
        'item_quantity': {
            'type': 'integer',
            'required': True
        },
        'vendor_item_id': {
            'type': 'string',
            'required': True
        },
        'vendor_name': {
            'type': 'string',
            'required': True
        },
        'vendor_site': {
            'type': 'string',
            'required': True,
            'url_or_blank': True
        }
    }

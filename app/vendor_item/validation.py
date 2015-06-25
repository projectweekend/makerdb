from app.utils.validation import BaseValidationMixin


class VendorItemValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'vendor_name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'vendor_item_id': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'quantity': {
            'type': 'integer',
            'required': True
        }
    }

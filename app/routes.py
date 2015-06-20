from app import api
from user import handlers as user_handlers
from inventory_item import handlers as Inventory_item_handlers


api.add_route('/v1/user', user_handlers.UserResource())
api.add_route('/v1/authenticate', user_handlers.AuthenticateResource())
api.add_route('/v1/inventory-item', Inventory_item_handlers.InventoryItemCollection())

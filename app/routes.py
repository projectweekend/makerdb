from app import api
from user import handlers as user_handlers
from inventory_item import handlers as inventory_handlers


api.add_route('/v1/user', user_handlers.UserResource())
api.add_route('/v1/authenticate', user_handlers.AuthenticationResource())
api.add_route('/v1/inventory-item', inventory_handlers.InventoryItemCollectionResource())
api.add_route('/v1/inventory-item/{item_id}', inventory_handlers.InventoryItemDetailResource())

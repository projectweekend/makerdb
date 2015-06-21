CREATE FUNCTION sp_inventory_items_update
(
    itemDoc JSON
)

RETURNS TABLE
(
    resultDoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH i as (
        UPDATE          app_inventory_items
        SET             name = CAST(itemDoc ->> 'name' AS TEXT),
                        url = CAST(itemDoc ->> 'url' AS TEXT),
                        image_url = CAST(itemDoc ->> 'image_url' AS TEXT),
                        quantity = CAST(itemDoc ->> 'quantity' AS INTEGER),
                        vendor_name = CAST(itemDoc ->> 'vendor_name' AS TEXT),
                        vendor_item_id = CAST(itemDoc ->> 'vendor_item_id' AS TEXT),
                        vendor_site = CAST(itemDoc ->> 'vendor_site' AS TEXT)
        WHERE           id = CAST(itemDoc ->> 'id' AS INTEGER) AND
                        user_id = CAST(itemDoc ->> 'user_id' AS INTEGER)
        RETURNING       app_inventory_items.id,
                        app_inventory_items.user_id,
                        app_inventory_items.name,
                        app_inventory_items.url,
                        app_inventory_items.image_url,
                        app_inventory_items.quantity,
                        app_inventory_items.vendor_name,
                        app_inventory_items.vendor_item_id,
                        app_inventory_items.vendor_site
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;

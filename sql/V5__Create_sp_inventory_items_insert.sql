CREATE FUNCTION sp_inventory_items_insert
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
        INSERT INTO     app_inventory_items
                        (
                            user_id,
                            name,
                            url,
                            image_url,
                            quantity,
                            vendor_name,
                            vendor_item_id,
                            vendor_site
                        )
        VALUES          (
                            CAST(itemDoc ->> 'user_id' AS INTEGER),
                            CAST(itemDoc ->> 'name' AS TEXT),
                            CAST(itemDoc ->> 'url' AS TEXT),
                            CAST(itemDoc ->> 'image_url' AS TEXT),
                            CAST(itemDoc ->> 'quantity' AS INTEGER),
                            CAST(itemDoc ->> 'vendor_name' AS TEXT),
                            CAST(itemDoc ->> 'vendor_item_id' AS TEXT),
                            CAST(itemDoc ->> 'vendor_site' AS TEXT)
                        )
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

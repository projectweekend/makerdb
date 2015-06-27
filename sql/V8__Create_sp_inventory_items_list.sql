CREATE FUNCTION sp_inventory_items_list
(
    itemDoc JSON
)

RETURNS TABLE
(
    record_count INTEGER,
    resultDoc JSON
) AS

$$
DECLARE         recordCount INTEGER;
BEGIN
    SELECT      COUNT(inv.id) INTO recordCount
    FROM        app_inventory_items AS inv
    WHERE       inv.user_id = CAST(itemDoc ->> 'user_id' AS INTEGER);

    RETURN      QUERY

    WITH i as (
        SELECT          app_inventory_items.id,
                        app_inventory_items.user_id,
                        app_inventory_items.name,
                        app_inventory_items.url,
                        app_inventory_items.image_url,
                        app_inventory_items.quantity,
                        app_inventory_items.vendor_name,
                        app_inventory_items.vendor_item_id
        FROM            app_inventory_items
        WHERE           app_inventory_items.user_id = CAST(itemDoc ->> 'user_id' AS INTEGER)
        ORDER BY        app_inventory_items.name
        OFFSET          CAST(itemDoc ->> 'skip' AS INTEGER)
        LIMIT           CAST(itemDoc ->> 'take' AS INTEGER)
    )
    SELECT      recordCount,
                ARRAY_TO_JSON(ARRAY_AGG(i.*))
    FROM        i;
END;
$$

LANGUAGE plpgsql;

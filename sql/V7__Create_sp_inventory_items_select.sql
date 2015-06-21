CREATE FUNCTION sp_inventory_items_select
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
        SELECT          app_inventory_items.id,
                        app_inventory_items.user_id,
                        app_inventory_items.name,
                        app_inventory_items.url,
                        app_inventory_items.image_url,
                        app_inventory_items.quantity,
                        app_inventory_items.vendor_name,
                        app_inventory_items.vendor_item_id,
                        app_inventory_items.vendor_site
        FROM            app_inventory_items
        WHERE           app_inventory_items.id = CAST(itemDoc ->> 'id' AS INTEGER) AND
                        app_inventory_items.user_id = CAST(itemDoc ->> 'user_id' AS INTEGER)
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;

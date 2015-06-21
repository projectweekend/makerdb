CREATE FUNCTION sp_inventory_items_delete
(
    itemDoc JSON
)

RETURNS BOOLEAN
AS

$$
BEGIN
    DELETE FROM     app_inventory_items
    WHERE           app_inventory_items.id = CAST(itemDoc ->> 'id' AS INTEGER) AND
                    app_inventory_items.user_id = CAST(itemDoc ->> 'user_id' AS INTEGER);
    RETURN          FOUND;
END;
$$

LANGUAGE plpgsql;

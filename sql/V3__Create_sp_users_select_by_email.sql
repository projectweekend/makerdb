CREATE FUNCTION sp_users_select_by_email
(
    userEmail VARCHAR(255)
)

RETURNS TABLE
(
    jdoc JSON
) AS $$

BEGIN
    RETURN      QUERY
    WITH i as (
        SELECT      app_users.id,
                    app_users.email,
                    app_users.password,
                    app_users.is_active,
                    app_users.is_admin
        FROM        app_users
        WHERE       app_users.email = userEmail
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END; $$ LANGUAGE plpgsql;

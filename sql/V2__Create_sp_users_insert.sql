CREATE FUNCTION sp_users_insert
(
    userEmail VARCHAR(255),
    userPassword VARCHAR(255)
)

RETURNS TABLE
(
    jdoc JSON
) AS $$

BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_users
                        (email, password)
        VALUES          (userEmail, userPassword)
        RETURNING       app_users.id,
                        app_users.email,
                        app_users.is_active,
                        app_users.is_admin
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END; $$ LANGUAGE plpgsql;
